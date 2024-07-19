from collections import defaultdict
from datetime import datetime, timezone


import pytz
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from timezonefinder import TimezoneFinder

from .forms import SearchCityForm
from .models import SearchHistory


def get_local_time(latitude, longitude):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
    if not timezone_str:
        raise ValueError('Не удалось определить часовой пояс')

    local_tz = pytz.timezone(timezone_str)
    local_time = (
        datetime.now(timezone.utc)
        .astimezone(local_tz)
        .strftime('%H:%M')
    )
    return local_time, local_tz


def get_weather_data(city_name):
    geocoding_api_url = (
        f'http://api.openweathermap.org/geo/1.0/direct?'
        f'q={city_name}&limit=1&appid={settings.OPENWEATHERMAP_API_KEY}'
    )
    try:
        response = requests.get(geocoding_api_url)
        response.raise_for_status()
        geocode_response = response.json()
    except requests.RequestException as error:
        return None, f'Ошибка при запросе геокодирования: {str(error)}', None

    if (
        not geocode_response
        or 'lat' not in geocode_response[0]
        or 'lon' not in geocode_response[0]
    ):
        return None, f'Город "{city_name}" не найден', None
    latitude = geocode_response[0]['lat']
    longitude = geocode_response[0]['lon']

    try:
        local_time, local_tz = get_local_time(latitude, longitude)
    except ValueError as error:
        return None, str(error), None

    weather_api_url = (
        f'https://api.open-meteo.com/v1/forecast?latitude={latitude}'
        f'&longitude={longitude}&hourly=temperature_2m'
    )
    try:
        response = requests.get(weather_api_url)
        response.raise_for_status()
        weather_data = response.json()
    except requests.RequestException as error:
        return None, f'Ошибка при запросе данных погоды: {str(error)}', None

    if 'hourly' in weather_data and 'time' in weather_data['hourly']:
        grouped_data = defaultdict(list)
        current_time = datetime.now(timezone.utc).astimezone(local_tz)
        for dt, temp in zip(
            weather_data['hourly']['time'],
            weather_data['hourly']['temperature_2m']
        ):
            datetime_obj = datetime.fromisoformat(
                dt.replace('Z', '+00:00')
            ).astimezone(local_tz)
            if datetime_obj >= current_time:
                date_str = datetime_obj.strftime('%d-%m-%Y (%A)')
                time_str = datetime_obj.strftime('%H:%M')
                grouped_data[date_str].append(
                    {'time': time_str,
                     'temperature': temp}
                )
        weather_data['hourly']['grouped'] = dict(grouped_data)
    else:
        weather_data['hourly'] = {'grouped': {}}
    return weather_data, None, local_time


def weather_view(request):
    last_city = None
    if request.user.is_authenticated:
        last_search = (
            SearchHistory.objects
            .filter(user=request.user)
            .order_by('-search_date')
            .first()
        )
        if last_search:
            last_city = last_search.city_name
    if request.method == 'POST':
        form = SearchCityForm(request.POST)
    else:
        form = SearchCityForm(initial={'city_name': last_city})
    if request.method == 'POST' and form.is_valid():
        city_name = form.cleaned_data['city_name']
        weather_data, error, local_time = get_weather_data(city_name)
        if error:
            form.add_error(None, error)
        if weather_data:
            SearchHistory.objects.create(
                user=(request.user if request.user.is_authenticated
                      else None),
                city_name=city_name
            )
            context = {
                'weather_data': weather_data,
                'city_name': city_name,
                'local_time': local_time
            }
            return render(request, 'weather/weather_result.html', context)
    return render(
        request,
        'weather/weather_form.html',
        {'form': form, 'last_city': last_city}
    )


@login_required
def get_history(request):
    history = SearchHistory.objects.filter(
        user=request.user
    )
    return render(request, 'weather/search_history.html', {'history': history})
