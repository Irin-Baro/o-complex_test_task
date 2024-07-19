from django.core.validators import RegexValidator


name_validator = RegexValidator(
    regex=r'^[а-яА-Яa-zA-ZёЁ\s\-]+$',
    message='Можно использовать только буквы!'
)
