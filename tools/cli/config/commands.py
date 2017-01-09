from collections import OrderedDict

"""
File containing the required options for each of the cli commands.

Uses an ordered dict in order to request input in the desired order.
"""
_cli_options = {
    "add_place": OrderedDict([
        ("env", {
            "default": "dev",
            "type": str,
            "validations": []
        }),
        ("latitude", {
            "default": 0.00000,
            "type": float,
            "validations": []
        }),
        ("longitude", {
            "default": 0.00000,
            "type": float,
            "validations": []
        })
    ])
}

def get_arguments(command, defined={}):
    return [(key, _cli_options[command][key]) for key in _cli_options[command] \
                       if key not in defined]