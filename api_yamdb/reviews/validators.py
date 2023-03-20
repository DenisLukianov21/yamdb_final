
from django.contrib.auth.validators import UnicodeUsernameValidator


class UsernameRegexValidator(UnicodeUsernameValidator):
    """Валидация имени пользователя."""

    regex = r'^[\w.@+-]+\Z'
    max_length = 225
    message = (f'Введите правильное имя пользователя. Оно может содержать'
               f' только буквы, цифры и знаки @/./+/-/_.'
               f' Длина не более {max_length} символов')
    error_messages = {
        'invalid': f'Набор символов не более {max_length}. '
                   'Только буквы, цифры и @/./+/-/_',
        'required': 'Поле не может быть пустым',
    }
