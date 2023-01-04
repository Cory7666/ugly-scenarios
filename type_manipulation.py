def __is_string(user_input: str) -> bool:
    return True


def __is_integer(user_input: str) -> bool:
    try:
        int(user_input)
        return True
    except ValueError:
        return False


def __is_decimal(user_input: str) -> bool:
    try:
        float(user_input)
        return True
    except ValueError:
        return False


type_check: dict = {
    "string": __is_string,
    "integer": __is_integer,
    "decimal": __is_decimal
}

type_cast: dict = {
    "string": lambda x: str(x),
    "integer": lambda x: int(x),
    "decimal": lambda x: float(x)
}
