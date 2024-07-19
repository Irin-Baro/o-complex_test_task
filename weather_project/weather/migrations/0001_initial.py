# Generated by Django 3.2.3 on 2024-07-18 15:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(help_text='Укажите название города', max_length=100, validators=[django.core.validators.RegexValidator(message='Можно использовать только буквы!', regex='^[а-яА-Яa-zA-ZёЁ\\s\\-]+$')], verbose_name='Название города')),
                ('search_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата поиска')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'История поиска',
                'ordering': ('-search_date',),
            },
        ),
    ]
