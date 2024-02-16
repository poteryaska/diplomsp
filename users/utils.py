import string
from django.utils.crypto import get_random_string


def create_digit_code() -> str:
    """
     Возвращает строку из 4-х случайных цифр.
    """
    return get_random_string(length=4, allowed_chars=string.digits)



