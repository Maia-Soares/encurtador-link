import re
import string
import random
from app.domain.exceptions import InvalidURLError

URL_REGEX = re.compile(
    r'^(?:http|https|ftp)://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def validate_url(url: str) -> str:
    if not URL_REGEX.match(str(url)):
        raise InvalidURLError(f"URL inválida: {url}")
    return url


def generate_slug() -> str:
    charset = string.ascii_letters + string.digits
    return ''.join(random.choices(charset, k=8))
