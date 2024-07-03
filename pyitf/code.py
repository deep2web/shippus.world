from typing import Tuple
from pyitf.check_digit import calculate_check_digit
from pyitf.internal import digits


def split_code(itf: int) -> Tuple[int, int]:
    """Returns the given itf code as tuple of it's main part and check digit."""
    *code_digits, checksum = digits(itf)

    code = 0
    for i, n in enumerate(reversed(code_digits)):
        code += n * 10**i

    return (code, checksum)


def validate_code(itf: int) -> bool:
    """Returns true if the given codes check digit matches it's main part."""
    code, chksum = split_code(itf)
    return calculate_check_digit(code) == chksum
