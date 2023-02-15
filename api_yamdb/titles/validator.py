from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(self, value):
        current_year = timezone.now().year
        if not value <= current_year:
            raise ValidationError(
                'Проверьте дату создания произведения'
            )
        return value
