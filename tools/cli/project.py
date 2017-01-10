"""
Command line tool to access services.
"""
from json import dumps
import click

from config.config import Config
from config.commands import get_arguments


_global_options = [
    click.option("--env", default="dev", help="environment")
]

def add_options(options):
    """
    Decorator to add a list of click options to command.
    """
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

def validate_input(value, validations):
    """
    Validates the value against the required validations.

    TODO: determine how validations will work with commands.py
    """
    return True

def typed_input(value, param):
    """
    Validate value to parameter specifications and convert to desired type.
    """
    converted = param["type"](value)

    if not validate_input(value, param["validations"]):
        raise ValidationError("Value not valid")

    return converted

def typed_default(param):
    """
    Get default value and convert to specified type.
    """
    return param["type"](param["default"])

def gather_parameters(params):
    """
    Requests parameter input from the user, uses default values if no input is received. 

    Validates and converts all inputs to defined types, returns dict.
    """
    inputs = {}
    for param in params:
        while param[0] not in inputs:
            value = input("{} [{}]: ".format(param[0].title(), param[1]["default"]))
            if len(value) == 0:
                value = typed_default(param[1])
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
    """
    Click group for all commands.
    """
    pass

""" Places API """
@click.command()
@add_options(_global_options)
def add_place(**kwargs):
    """
    Add place endpoint: /add
    """
    click.echo("adding place")
    args = gather_parameters(get_arguments("add_place", kwargs))

    click.echo(dumps(args, indent=4))


cli.add_command(add_place)

if __name__ == "__main__":
    cli()
