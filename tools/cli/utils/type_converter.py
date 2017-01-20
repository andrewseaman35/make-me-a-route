"""Module to handle conversion of user input to typed values."""
from sys import argv, exit as sysexit

# Map of type names to types for command line usage
_TYPE_MAPPING = {
    "bool": bool,
    "float": float,
    "list": list,
    "int": int,
    "str": str,
}

# The types that we will cast directly
_CASTABLE_TYPES = [bool, int, float, str]


def convert(value, to_type):
    """Converts the given value to the given type.
    Intended for handling of user input strings.

    Raises:
       ValueError if conversion cannot be performed.
    """
    if to_type in _CASTABLE_TYPES:
        typed_value = _cast(value, to_type)
    elif to_type == list:
        typed_value = _to_list(value)
    return typed_value


def _cast(value, to_type):
    """Handles the following:
    bool, int, float, str.
    """
    return to_type(value)


def _to_list(value, inner_type=str):
    """Handles conversion to list of given inner_type..
    Value must be comma separated list. Spaces in between elements are stripped
    before converting to inner_type.
    """
    elements = [convert(word.strip(), inner_type) for word in value.split(",")]
    return elements


if __name__ == "__main__":
    """If run independently, convert arg1 to type in arg2."""
    try:
        value = argv[1]
        to_type = argv[2]
    except IndexError:
        print("Usage: python type_converter.py <value> <convert_to_type>")
        sysexit(1)

    try:
        to_type = _TYPE_MAPPING[to_type]
    except KeyError:
        print("Type mapping not found for {}".format(to_type))
        sysexit(1)

    convert(value, to_type)
