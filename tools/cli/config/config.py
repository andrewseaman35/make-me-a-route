from configparser import ConfigParser
from sys import argv
from json import dumps

from config.constants import CONFIG_FILE

ENVIRONMENTS = ["local", "dev", "test", "green", "blue"]

class Config():
    def __init__(self, environment):
        self._config = ConfigParser()
        self._config.read(CONFIG_FILE)

        if environment.lower() not in ENVIRONMENTS:
            environment = "dev"

        self.places_url = str(self._config.get(environment, "PlacesURL"))
        self.place_tags_url = str(self._config.get(environment, "PlaceTagsURL"))

    def __str__(self):
        config_dict = self.__dict__
        del config_dict["_config"]
        return dumps(config_dict, indent=4)

if __name__ == "__main__":
    """
    If we run this directly, print out the configuration for the passed in environment.

    python config.py <local|dev|test|green|blue>
    """
    try:
        environment = argv[1]
    except IndexError:
        environment = "dev"
    config = Config(environment)
    print("Configuration for {} environment".format(environment))
    print(str(config))