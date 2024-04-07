import re


def validate_string(min_length=3, max_length=50, pattern=r"^[a-zA-Z]+(?:\s?[a-zA-Z]+)*$", allow_none=False):
    def decorator(setter):
        def wrapper(self, value):
            if allow_none and value is None:
                return setter(self, value)
            if not isinstance(value, str):
                raise ValueError(f'ERROR: {value} must be str type')
            if not (min_length < len(value) <= max_length):
                raise ValueError(f"ERROR: {value} must be between {min_length} and {max_length} characters")
            if not re.match(pattern, value):
                raise ValueError(f"ERROR: {value} must match pattern {pattern}")
            return setter(self, value)
        return wrapper
    return decorator


