from http import HTTPStatus
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse

from weather.forms import SearchCityForm
from weather.models import SearchHistory


class TestGetHistoryView(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        cls.url = reverse('weather:search-history')

        cls.search_history_objects = [
            SearchHistory(user=cls.user, city_name='Moscow'),
            SearchHistory(user=cls.user, city_name='London')
        ]
        SearchHistory.objects.bulk_create(cls.search_history_objects)

    @classmethod
    def setUp(self):
        cache.clear()
        self.unauthorized_user = Client()
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_get_history_logged_in(self):
        """Проверка, что авторизованный пользователь
        получает историю своего поиска.
        """
        response = self.authorized_user.get(self.url)
        history = response.context.get('history')
        self.assertEqual(
            len(history),
            len(self.search_history_objects)
        )
        self.assertEqual(history[0].city_name, 'Moscow')
        self.assertEqual(history[1].city_name, 'London')

    def test_get_no_history(self):
        """Проверка, что неавторизованный пользователь
        не получает историю поиска.
        """
        SearchHistory.objects.filter(user=self.user).all().delete()
        response = self.authorized_user.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        history = response.context['history']
        self.assertEqual(len(history), 0)


class WeatherViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        cls.url = reverse('weather:weather-view')

    @classmethod
    def setUp(self):
        cache.clear()
        self.unauthorized_user = Client()
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_get_request(self):
        """Проверка контекста в шаблоне weather_form."""
        response = self.unauthorized_user.get(self.url)
        self.assertIsInstance(response.context['form'], SearchCityForm)

    def test_post_request_with_invalid_form(self):
        """Проверка корректности формы с пустым запросом."""
        response = self.unauthorized_user.post(self.url, {'city_name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/weather_form.html')
        self.assertContains(response, 'Обязательное поле.')

    @patch('weather.views.get_weather_data')
    def test_post_request_with_valid_form(self, mock_get_weather_data):
        """Проверка корректности формы с правильным запросом."""
        weather_data = {
            'hourly': {
                'grouped': {
                    '08-07-2024 (четверг)': [
                        {'time': '14:00', 'temperature': '20°C'}
                    ]
                }
            }
        }
        mock_get_weather_data.return_value = (
            weather_data,
            None,
            weather_data.get('time')
        )
        response = self.authorized_user.post(
            self.url,
            {'city_name': 'Moscow'}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'weather/weather_result.html')
        self.assertContains(response, 'Moscow')
        self.assertContains(response, '20°C')
        self.assertContains(response, '14:00')
        self.assertTrue(
            SearchHistory.objects
            .filter(user=self.user, city_name='Moscow')
            .exists()
        )

    @patch('weather.views.get_weather_data')
    def test_post_request_with_error(self, mock_get_weather_data):
        """Проверка корректности формы с неправильным запросом."""
        mock_get_weather_data.return_value = (None, 'Город не найден', None)
        response = self.unauthorized_user.post(
            self.url,
            {'city_name': 'InvalidCity123'}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'weather/weather_form.html')
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('Можно использовать только буквы!', str(form.errors))
        self.assertFalse(
            SearchHistory.objects
            .filter(city_name='InvalidCity123')
            .exists()
        )
