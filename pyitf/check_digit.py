import internal as internal


def calculate_check_digit(code: int) -> int:
    """Calculates and returns the check digit for the given code."""
    digits = internal.digits(code)

    sum_digits = 0
    for i, n in enumerate(digits):
        sum_digits += n if (i+1) % 2 == 0 else n*3

    mod10 = sum_digits % 10

    return 0 if mod10 < 1 else 10-mod10


def append_check_digit(code: int) -> int:
    """Returns the given code including a calculated check digit."""
    return code*10 + calculate_check_digit(code)
