from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CitySearchCountView

app_name = 'api'

API_VERSION = 'v1'

router = DefaultRouter()
urlpatterns = [
    path(
        f'{API_VERSION}/city-search-count/',
        CitySearchCountView.as_view(),
        name='city-search-count'
    ),
]
