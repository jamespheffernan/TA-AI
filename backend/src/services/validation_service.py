def validate_int(value, name):
    """Ensure value is a positive integer"""
    try:
        val = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be an integer")
    if val <= 0:
        raise ValueError(f"{name} must be positive")
    return val


def validate_str(value, name, allow_empty=False):
    """Ensure value is a string and optionally non-empty"""
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    v = value.strip()
    if not allow_empty and not v:
        raise ValueError(f"{name} cannot be empty")
    return v