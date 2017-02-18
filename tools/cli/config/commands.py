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
        ("name", {
            "type": str,
            "validations": [
                ("longer_than", 3)
            ]
        }),
        ("place_type", {
            "default": "general",
            "type": str,
            "validations": [
                ("longer_than", 3)
            ]
        }),
        ("description", {
            "default": "No description",
            "type": str,
            "validations": []
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
    ]),
    "get_places_in_range": OrderedDict([
        ("env", {
            "default": "dev",
            "type": str,
            "validations": [
                ("in", ["dev", "test", "green", "blue", "local"])
            ]
        }),
        ("latitude", {
            "default": 0.0,
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
        }),
        ("radius", {
            "default": 10.0,
            "type": float,
            "validations": [
                ("greater_than", 0)
            ]
        })
    ]),
    "delete_place_by_id": OrderedDict([
        ("env", {
            "default": "dev",
            "type": str,
            "validations": [
                ("in", ["dev", "test", "green", "blue", "local"])
            ]
        }),
        ("id", {
            "type": str
        })
    ]),
    "get_places_by_id": OrderedDict([
        ("env", {
            "default": "dev",
            "type": str,
            "validations": [
                ("in", ["dev", "test", "green", "blue", "local"])
            ]
        }),
        ("ids", {
            "type": list,
            "validations": []
        })
    ]),
    "add_place_tag": OrderedDict([
        ("env", {
            "default": "dev",
            "type": str,
            "validations": [
                ("in", ["dev", "test", "green", "blue", "local"])
            ]
        }),
        ("name", {
            "type": str,
            "valdations": [
                ("longer_than", 3)
            ]
        }),
        ("description", {
            "default": "No description",
            "type": str,
            "validations": [
                ("longer_than", 3)
            ]
        })
    ]),
    "get_place_tags_by_id": OrderedDict([
        ("env", {
            "default": "dev",
            "type": str,
            "validations": [
                ("in", ["dev", "test", "green", "blue", "local"])
            ]
        }),
        ("ids", {
            "type": list,
            "validations": []
        })
    ]),
}

def get_arguments(command, defined={}):
    """Returns a list of tuples specifying the required arguments for the given action
    and argument specifications. Excludes any arguments that are in `defined`.
    """
    return [(key, _cli_options[command][key]) for key in _cli_options[command] \
                       if key not in defined]
