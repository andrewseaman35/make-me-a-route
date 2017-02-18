"""
Command line tool to access services.
"""
# Standard Imports #
import sys
from json import dumps

# Nonstandard Imports #
import click
from py_value_validator.value_validator import ValueValidator, ValidationError

# Local Imports #
from config.config import Config
from config.commands import get_arguments
from utils.utils import stringify_dict
from utils.type_converter import convert
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
    """Validate value to parameter specifications and convert to desired type.
    List: assume that values are comma separated, strip spaces
    """
    try:
        converted = convert(value, param["type"])
    except KeyError:
        click.echo("Type must be defined in commands.py")
        sys.exit(1)

    validate_value(converted, param.get("validations", []))

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
                default = param[1].get("default", None)
                out = "{}".format(param[0])
                if default is not None:
                    out += " [{}]".format(default)
                value = input(out + ": ")
                if len(value) == 0:
                    if default is None:
                        click.echo("No default value available")
                        continue
                    value = default
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


""" Place Tags API """
@click.command()
@add_options(_global_options)
def add_place_tag(**kwargs):
    """Add place tag endpoint: /add"""
    action_name = "add_place_tag"

    # Remove all kwargs that were not inputted and gather the rest
    filtered_kwargs = {key: kwargs[key] for key in kwargs if kwargs[key] is not None}
    args = gather_parameters(filtered_kwargs, get_arguments(action_name))

    url = Config(args['env']).place_tags_url + "add"
    del args['env']
    args = stringify_dict(args)

    click.echo(dumps(http_request("post", url, args).json, indent=4))


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
    args = stringify_dict(args)

    click.echo(dumps(http_request("post", url, args).json, indent=4))


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
    args = stringify_dict(args)

    click.echo(dumps(http_request("post", url, args).json, indent=4))

@click.command()
@add_options(_global_options)
def delete_place_by_id(**kwargs):
    """Delete place endpoint: /delete"""
    action_name = "delete_place_by_id"

    # Remove all kwargs that were not inputted and gather the rest
    filtered_kwargs = {key: kwargs[key] for key in kwargs if kwargs[key] is not None}
    args = gather_parameters(filtered_kwargs, get_arguments(action_name))

    url = Config(args['env']).places_url + "delete_by_ids"
    del args['env']
    args = stringify_dict(args)

    click.echo(dumps(http_request("post", url, args).json, indent=4))

@click.command()
@add_options(_global_options)
def get_places_by_id(**kwargs):
    """Get places by id endpoint: /get_by_ids [POST]"""
    action_name = "get_places_by_id"

    # Remove all kwargs that were not inputted and gather the rest
    filtered_kwargs = {key: kwargs[key] for key in kwargs if kwargs[key] is not None}
    args = gather_parameters(filtered_kwargs, get_arguments(action_name))

    url = Config(args['env']).places_url + "get_by_ids"
    del args['env']

    click.echo(dumps(http_request("post", url, args).json, indent=4))

""" Place Tags API """
cli.add_command(add_place_tag)

""" Places API """
cli.add_command(add_place)
cli.add_command(get_places_in_range)
cli.add_command(delete_place_by_id)
cli.add_command(get_places_by_id)

if __name__ == "__main__":
    cli()
