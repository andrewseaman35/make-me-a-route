class ValidationError(Exception):
    """
    Raised when values do not pass value validation.
    """
    pass

class ParseError(Exception):
    """
    Raised when parsing fails.
    """
    pass
