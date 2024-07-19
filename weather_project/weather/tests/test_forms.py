from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse

from weather.models import SearchHistory


class SearchCityFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        cls.url = reverse('weather:weather-view')

        cls.search_history = SearchHistory.objects.create(
            user=cls.user,
            city_name='Moscow',
        )

    @classmethod
    def setUp(self):
        cache.clear()
        self.unauthorized_user = Client()
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_last_city_in_form_initial_for_authenticated_user(self):
        """Проверка, что последний запрошенный город попадает
        в форму авторизованного пользователя.
        """
        response = self.authorized_user.get(self.url)
        last_city = response.context['form'].initial.get('city_name')
        self.assertEqual(last_city, self.search_history.city_name)

    def test_no_city_in_form_initial_for_unauthenticated_user(self):
        """Проверка, что у неавторизованного пользователя
        название города отсутствует в форме.
        """
        response = self.unauthorized_user.get(self.url)
        last_city = response.context['form'].initial.get('city_name')
        self.assertIsNone(last_city)
