"""
Command line tool to access services.
"""
from json import dumps
import click

from config.config import Config
from config.commands import get_arguments
from utils.py_value_validator.value_validator import ValueValidator, ValidationError
from utils.validator_functions import ValidatorFunctions
from utils.request_handler import http_request

_global_options = [
    click.option("--env", help="environment")
]

_validator_functions = ValidatorFunctions()
_validator = ValueValidator(_validator_functions)

def add_options(options):
    """Decorator to add a list of click options to command."""
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

def get_user_id():
    """Gets user id.

    TODO: after authentication is in place, get this working properly.
    """
    return "cli_user"

def validate_value(value, validations):
    """Validates the value against the required validations.

    Raises:
       ValidationError if any validation does not pass
    """
    _validator.validate(value, validations)

def typed_input(value, param):
    """Validate value to parameter specifications and convert to desired type."""
    converted = param["type"](value)

    validate_value(converted, param["validations"])

    return converted

def typed_default(param):
    """Get default value and convert to specified type."""
    default_value = param.get("default", None)
    return None if default_value is None else param["type"](default_value)

def gather_parameters(kwargs, params):
    """Requests parameter input from the user, uses default values if no input is received. 

    Validates and converts all inputs to defined types, returns dict.
    """
    inputs = {
        'user_id': get_user_id()
    }
    for param in params:
        while param[0] not in inputs:
            if param[0] not in kwargs:
                default = typed_default(param[1])
                out = "{}".format(param[0])
                if default is not None:
                    out += " [{}]".format(default)
                value = input(out + ": ")
                if len(value) == 0:
                    if default is None:
                        click.echo("No default value available")
                        continue
                    value = typed_default(param[1])
            else:
                value = kwargs[param[0]]
                del kwargs[param[0]]
            try:
                value = typed_input(value, param[1])
                inputs[param[0]] = value
            except ValueError:
                click.echo("Required type: {}".format(param[1]["type"].__name__))
            except ValidationError as validation_error:
                click.echo(validation_error)
    return inputs

@click.group()
def cli(**kwargs):
    """Click group for all commands."""
    pass

""" Places API """
@click.command()
@add_options(_global_options)
def add_place(**kwargs):
    """Add place endpoint: /add"""
    action_name = "add_place"

    # Remove all kwargs that were not inputted and gather the rest
    filtered_kwargs = {key: kwargs[key] for key in kwargs if kwargs[key] is not None}
    args = gather_parameters(filtered_kwargs, get_arguments(action_name))

    url = Config(args['env']).places_url + "add"
    del args['env']

    click.echo(dumps(http_request("post", url, args), indent=4))

@click.command()
@add_options(_global_options)
def get_places_in_range(**kwargs):
    """Add place endpoint: /get_by_distance"""
    action_name = "get_places_in_range"

    # Remove all kwargs that were not inputted and gather the rest
    filtered_kwargs = {key: kwargs[key] for key in kwargs if kwargs[key] is not None}
    args = gather_parameters(filtered_kwargs, get_arguments(action_name))

    url = Config(args['env']).places_url + "get_by_distance"
    del args['env']

    click.echo(dumps(http_request("post", url, args), indent=4))

cli.add_command(add_place)
cli.add_command(get_places_in_range)

if __name__ == "__main__":
    cli()
