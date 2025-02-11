import re


def is_valid_input(text: str) -> bool:
    pattern = r"^[a-zA-Z0-9_-]+$"
    return bool(re.match(pattern, text))
