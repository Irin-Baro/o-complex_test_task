from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from weather.models import SearchHistory
from .serializers import CitySearchCountSerializer


class CitySearchCountView(APIView):
    """Представление для подсчета запросов городов."""

    def get(self, request, *args, **kwargs):
        search_counts = (
            SearchHistory.objects
            .values('city_name')
            .annotate(search_count=Count('city_name'))
            .order_by('-search_count')
        )
        serializer = CitySearchCountSerializer(search_counts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
