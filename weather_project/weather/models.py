from django.contrib.auth.models import User
from django.db import models

from core import constants
from . import validators


class SearchHistory(models.Model):
    """Модель истории поиска."""

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    city_name = models.CharField(
        max_length=constants.MAX_NAME_LENGTH,
        validators=(validators.name_validator,),
        verbose_name='Название города',
        help_text='Укажите название города'
    )
    search_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата поиска'
    )

    class Meta:
        ordering = ('-search_date',)
        verbose_name = 'История поиска'

    def __str__(self):
        return f'{self.user.username} - {self.city_name} - {self.search_date}'
