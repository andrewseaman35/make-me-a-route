import requests
from json import dumps

from .exceptions import EndpointNotDefinedError, EnvironmentNotDefinedError
from .utils import stringify_dict
from config.config import Config

def http_request(method, url, params=None):
    """Forwards the request to the appropriate function.

    All responses are returned as dict.

    NOTE: Leave this here until it is confirmed to be unnecessary.
    """
    if method.lower() not in _request_methods:
        raise NotImplementedError("HTTP request method not implemented")

    # Endpoints expect all values to come in as strings
    string_params = stringify_dict(params)

    return _request_methods[method.lower()](url, string_params)

def _get_request(url, params):
    """Opens a get request with params specifying a query string."""
    request = requests.get(url, params=params)

    return request.json()

def _post_request(url, params):
    """Opens a post request for the given endpoint and parameters."""
    data = dumps(params).encode("utf-8")
    request = requests.post(url, data=data)
    return request.json()

_request_methods = {
    "get": _get_request,
    "post": _post_request,
}