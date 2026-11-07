import re
from urllib.parse import urlparse

SUSPICIOUS_KEYWORDS = ["login", "verify", "secure", "update", "bank", "confirm", "otp", "payment", "claim", "prize", "click", "win"]


def extract_url_features(url: str):
    parsed = urlparse(url)
    hostname = parsed.netloc.lower()
    path = parsed.path.lower()
    query = parsed.query.lower()
    hostname_without_port = hostname.split(":")[0]
    dots = hostname_without_port.count(".")
    subdomain_count = max(0, dots - 1)
    url_length = len(url)
    hostname_length = len(hostname_without_port)
    has_https = parsed.scheme == "https"
    is_ip_host = bool(re.fullmatch(r"(\d{1,3}\.){3}\d{1,3}", hostname_without_port))
    suspicious_keywords = [keyword for keyword in SUSPICIOUS_KEYWORDS if keyword in (hostname + path + query)]
    special_char_count = len(re.findall(r"[^A-Za-z0-9/]", url))
    digits_count = sum(ch.isdigit() for ch in url)
    hyphen_count = url.count("-")
    path_length = len(path)
    query_length = len(query)
    has_at_symbol = "@" in url
    has_encoded_chars = "%" in url
    return {
        "url_length": url_length,
        "hostname_length": hostname_length,
        "dots_count": dots,
        "subdomain_count": subdomain_count,
        "special_char_count": special_char_count,
        "digits_count": digits_count,
        "hyphen_count": hyphen_count,
        "has_https": has_https,
        "is_ip_host": is_ip_host,
        "has_at_symbol": has_at_symbol,
        "has_encoded_chars": has_encoded_chars,
        "path_length": path_length,
        "query_length": query_length,
        "suspicious_keywords": suspicious_keywords,
    }
