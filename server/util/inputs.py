import re

def sanitise_string(string: str) -> str:
    """
    This function sanitises a string, by lowercasing it and removing any leading or trailing whitespace.
    """
    return string.lower().strip()

def is_input_invalid(input: str) -> bool:
    """
    This function checks if an input contains invalid characters, so that
    we can avoid SQL injection attacks.
    """
    invalid_chars = [";", "--", ":", "*", "/", "\\"]
    for char in invalid_chars:
        if char in input:
            return True
    return False

def is_email_valid(email: str) -> bool:
    """
    This function checks if an email is valid.
    """
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def valid_num(input: str, min: int, max: int) -> bool:
    """
    This function checks if a number is within a valid range and is a valid number.
    """
    print(input)
    print(min)
    print(max)
    try:
        num = int(input)
        if num >= min and num <= max:
            return True
    except ValueError:
        return False
    return False