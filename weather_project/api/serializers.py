from rest_framework import serializers


class CitySearchCountSerializer(serializers.Serializer):
    """Сериализатор подсчета запросов городов."""

    city_name = serializers.CharField()
    search_count = serializers.IntegerField()
