import re


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> bool:
    return len(password) >= 8


def validate_rating(value, field_name: str = "value"):
    """Ensure value is between 1 and 10."""
    try:
        val = int(value)
        if 1 <= val <= 10:
            return val, None
        return None, f"'{field_name}' must be between 1 and 10"
    except (TypeError, ValueError):
        return None, f"'{field_name}' must be an integer"
