class ParseError(Exception):
    """Raised when parsing fails."""
    pass

class EndpointNotDefinedError(Exception):
    """Raised no endpoint is found for a specified action and environment"""
    pass

class EnvironmentNotDefinedError(Exception):
    """Raised if no environment is defined while making request"""
    pass
