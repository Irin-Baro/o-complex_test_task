from django.urls import path

from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.weather_view, name='weather-view'),
    path('history/', views.get_history, name='search-history'),
]
