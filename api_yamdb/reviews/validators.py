import re

from django.core.exceptions import ValidationError


def me_username_forbidden_validator(value):
    """Проверяем, что юзернейм не соответствует занятому 'me'."""
    if value.lower() == "me":
        raise ValidationError("Использование этого никнейма запрещено.")


def username_validator(value):
    """Проверяем юзернейм на соответствие паттерну."""
    pattern = r"^^[\w.@+-]+\Z"
    if not re.search(pattern, value):
        raise ValidationError("Некорректный никнейм.")
