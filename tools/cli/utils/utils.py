def stringify_dict(values):
    """Converts all values in dictionary to strings."""
    return {key: str(values[key]) for key in values}