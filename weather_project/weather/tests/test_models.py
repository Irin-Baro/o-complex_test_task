from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from core import constants
from weather.models import SearchHistory

User = get_user_model()


class SearchHistoryModelTest(TestCase):
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

    def test_create_search_history(self):
        """"Проверка создания модели SearchHistory."""
        self.assertEqual(self.search_history.user.username, 'testuser')
        self.assertEqual(self.search_history.city_name, 'Moscow')

    def test_models_have_correct_object_names(self):
        """Проверка, что у моделей корректно работает __str__."""
        self.assertEqual(
            str(self.search_history),
            (f'{self.user.username} - Moscow - '
             f'{self.search_history.search_date}')
        )

    def test_city_name_length(self):
        """Проверка ограничения по длине названия города."""
        long_city_name = 'a' * (constants.MAX_NAME_LENGTH + 1)
        with self.assertRaises(ValidationError):
            SearchHistory(
                user=self.user,
                city_name=long_city_name
            ).full_clean()

    def test_city_name_empty(self):
        """Проверка отсутствия названия города."""
        empty_city_name = ''
        with self.assertRaises(ValidationError):
            SearchHistory(
                user=self.user,
                city_name=empty_city_name
            ).full_clean()

    def test_city_name_validator(self):
        """Проверка валидации названия города."""
        invalid_city_name = 'InvalidCity123'
        with self.assertRaises(ValidationError):
            SearchHistory(
                user=self.user,
                city_name=invalid_city_name
            ).full_clean()

    def test_search_history_verbose_name(self):
        """Verbose_name в полях модели совпадает с ожидаемым."""
        field_verboses = [
            ('city_name', 'Название города'),
            ('search_date', 'Дата поиска'),
        ]
        for field, expected_value in field_verboses:
            with self.subTest(field=field):
                self.assertEqual(
                    self.search_history._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_search_history_help_text(self):
        """Help_text в полях модели совпадает с ожидаемым."""
        field_help_texts = [
            ('city_name', 'Укажите название города'),
        ]
        for field, expected_value in field_help_texts:
            with self.subTest(field=field):
                self.assertEqual(
                    self.search_history._meta.get_field(field).help_text,
                    expected_value
                )

    def test_search_history_ordering(self):
        """Проверка сортировки объектов SearchHistory по дате поиска."""
        search_history_objects = [
            SearchHistory(user=self.user, city_name='London'),
            SearchHistory(user=self.user, city_name='Paris'),
        ]
        SearchHistory.objects.bulk_create(search_history_objects)
        history = SearchHistory.objects.all()
        self.assertEqual(history[0].city_name, 'Paris')
        self.assertEqual(history[1].city_name, 'London')
        self.assertEqual(history[2].city_name, 'Moscow')
