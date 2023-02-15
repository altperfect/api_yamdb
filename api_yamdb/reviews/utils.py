import random
import string


def generate_confirmation_code(size: int = 32) -> str:
    """Функция генерирует случайный 32-значный код подтверждения."""
    return ''.join(
        random.SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase
            + string.digits) for _ in range(size))
