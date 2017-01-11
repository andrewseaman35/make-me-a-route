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
            "validations": [
                ("in", ["dev", "test", "green", "blue", "local"])
            ]
        }),
        ("latitude", {
            "default": 0.00000,
            "type": float,
            "validations": [
                ("less_than_equal", 90),
                ("greater_than_equal", -90)
            ]
        }),
        ("longitude", {
            "default": 0.00000,
            "type": float,
            "validations": [
                ("less_than_equal", 90),
                ("greater_than_equal", -90)
            ]
        })
    ])
}

def get_arguments(command, defined={}):
    return [(key, _cli_options[command][key]) for key in _cli_options[command] \
                       if key not in defined]