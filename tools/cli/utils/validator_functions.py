from utils.py_value_validator.value_validator import GenericValidatorFunctions

class ValidatorFunctions(GenericValidatorFunctions):
    def add_typed_functions(self):
        self._add_function(str, "in", string_in)


"""String Functions"""
def string_in(mine, yours):
    return mine in yours