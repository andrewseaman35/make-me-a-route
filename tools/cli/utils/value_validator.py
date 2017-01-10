from sys import argv, exit as sys_exit
from functools import partial

class ValueValidator():
    def __init__(self, value):
        self._value = value
        self._functions = ValidatorFunctions(self._value)

    def validated(self, func_name, compare_to):
        """Performs a single validation."""
        return self._functions.get(func_name)(compare_to)

class ValidatorFunctions():
    def __init__(self, value):
        self._value = value
        self._functions = {
            'generic': {
                'less_than': self._value.__lt__,
                'greater_than': self._value.__gt__,
                'equal_to': self._value.__eq__,
            },
            str: {
            }
        }

    def _default(self, **kwargs):
        """Returned function if validator function is not found.

        Raises:
           NotImplementedError always
        """
        raise NotImplementedError("Comparison function not found for type {}: {}".format(
            kwargs['val_type'],
            kwargs['fun_name']
            ))

    def get(self, name):
        """
        Returns the requested function for the type of _value.
        First checks _functions[type], if not found, checks _functions['generic'].
        """
        func = self._functions.get(type(self._value), {}).get(name, None)
        func = func or self._functions['generic'].get(name, None)
        func = func or partial(self._default, val_type=type(self._value), fun_name=name)
        return func

    def get_function_list(self, value_type=None):
        """
        Returns a list of the functions defined for the stored value. Value type can be
        specified as value_type argument.
        """
        return self._functions.get(value_type or type(self._value), {}).keys()

    def list_all(self):
        """
        Lists all functions associated with a given value.
        """
        typed_functions = self.get_function_list()
        generic_functions = self.get_function_list('generic')

        final_functions = list(typed_functions)
        final_functions.extend((gf + " (generic)" for gf in generic_functions if gf not in typed_functions))

        print("--    Generic Functions    --")
        for function in generic_functions:
            print(function)

        print()
        print("-- Type-Specific Functions --")
        for function in typed_functions:
            print(function)

        print()
        print("--      Function List      --")
        for function in final_functions:
            print(function)

        print()


def get_typed_value_from_name(name):
    """
    Converts string of type name to value of that type.

    Raises:
       ValueError if type name not defined
    """
    types = {
        'str': "string",
        'int': 1,
        'float': 1.0,
        'dict': {'key': "value"},
        'list': ["list"],
        'type': type,
        'complex': (1+0j),
        'bytes': b'u',
        'tuple': ("tu", "ple"),
        'set': {"set"}
    }
    if name.lower() not in types:
        raise ValueError("No type found for {}".format(name.lower()))

    return types[name.lower()]

def main():
    """
    Runs if file is run independently.
    """
    try:
        _type = argv[1]
        _value = get_typed_value_from_name(_type)
    except ValueError as _value_error:
        print(str(_value_error))
        return 1
    except IndexError:
        print("Usage: python value_validator.py <type>")
        return 2

    functions = ValidatorFunctions(_value)
    functions.list_all()


if __name__ == "__main__":
    """
    If we run this directly, print out the function list for the passed type.abs

    python value_validator.py <type>
    """
    sys_exit(main())
