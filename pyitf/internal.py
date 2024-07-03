from typing import Any, List


def digits(code: Any) -> List[int]:
    if isinstance(code, str):
        string_code = code
    elif isinstance(code, int):
        string_code = str(code)
    else:
        raise Exception('unsupported type', code.__class__)

    if len(string_code) < 2:
        raise Exception('codes must be at least 2 digits long')

    return [int(char) for char in string_code]
