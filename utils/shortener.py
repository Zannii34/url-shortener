import secrets
import string

ALPHABET = string.ascii_letters + string.digits


def generate_short_code(length: int = 6) -> str:
    """Generate a URL-safe, non-sequential short code."""
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))


def is_valid_url(url: str) -> bool:
    """Basic validation for URLs."""
    if not url or len(url) > 2048:
        return False
    return url.startswith(('http://', 'https://'))
