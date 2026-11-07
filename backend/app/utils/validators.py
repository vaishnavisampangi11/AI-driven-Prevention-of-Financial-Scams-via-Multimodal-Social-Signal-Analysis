import re
from urllib.parse import urlparse


def clean_input(value: str) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def is_valid_url(value: str) -> bool:
    if not value or not isinstance(value, str):
        return False
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"}:
        return False
    if not parsed.netloc:
        return False
    return True


def safe_text_length(text: str, max_len: int = 4000) -> bool:
    return len(text) <= max_len
