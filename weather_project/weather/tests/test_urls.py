from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse

from weather.models import SearchHistory

User = get_user_model()


class PostUrlTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        cls.search_history = SearchHistory.objects.create(
            user=cls.user,
            city_name='Moscow',
        )

    def setUp(self):
        self.unauthorized_user = Client()
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_url_matches_page_name(self):
        """Соответствие адресов страниц их именам."""
        urls_for_page_names = [
            ('/', reverse('weather:weather-view')),
            ('/history/', reverse('weather:search-history')),
        ]
        for url, reverse_name in urls_for_page_names:
            with self.subTest(url=url):
                self.assertEqual(url, reverse_name)

    def test_urls_available_to_any_user(self):
        """Проверка доступности страниц пользователям."""
        urls_for_users = [
            (reverse('weather:weather-view'),
                HTTPStatus.OK, False),
            (reverse('weather:search-history'),
                HTTPStatus.OK, True),
        ]
        for reverse_name, http_status, need_auth in urls_for_users:
            with self.subTest(reverse_name=reverse_name):
                if not need_auth:
                    response = self.unauthorized_user.get(reverse_name)
                else:
                    response = self.authorized_user.get(reverse_name)
                self.assertEqual(response.status_code, http_status)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        cache.clear()
        templates_url_names = [
            (reverse('weather:weather-view'), 'weather/weather_form.html'),
            (reverse('weather:search-history'), 'weather/search_history.html'),
        ]
        for reverse_name, template in templates_url_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_user.get(reverse_name)
                self.assertTemplateUsed(response, template)
