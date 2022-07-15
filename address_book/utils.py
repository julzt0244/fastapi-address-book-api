import humps


def to_camel_case(value: str) -> str:
    return humps.camelize(value)
