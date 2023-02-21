import re

from django.core.exceptions import ValidationError

from api_yamdb.settings import RESERVED_USERNAMES


def forbidden_username_validator(value):
    """Проверяем, что юзернейм не относится к служебным."""
    if value.lower() in RESERVED_USERNAMES:
        raise ValidationError("Использование этого никнейма запрещено.")


def username_validator(value):
    """Проверяем юзернейм на соответствие паттерну."""
    pattern = r"^[\w.@+-]+\Z"
    if not re.search(pattern, value):
        raise ValidationError(
            (
                "Некорректный никнейм. Можно использовать латиницу, "
                "цифры и спец. символы: !\"#$%&'()*+,-./"
            )
        )
