"""
A command line tool to help maintain versioning of the services in this project.
"""
import os
import sys
import pickle

import datetime

from argparse import ArgumentParser


VERSION_FILE = "versions.pic"


def initialize_arguments(parser):
    """
    Initializes command line arguments.

    service: the service to use
    action: the action to run
    """
    parser.add_argument("-s", "--service", dest="service")
    parser.add_argument("-a", "--action", dest="action")


def validate_arguments(args):
    """
    Validates for required arguments:
      action
      service (only required if action is performed on version)
    """
    if args.action is None:
        print("Action must be defined (--action)")
        return False
    if args.action in ["get", "patch", "minor", "major"]:
        if args.service is None:
            print("Service must be defined (--service)")
            return False

    return True


def update_metadata(metadata):
    """
    Updates relevant portions of version file metadata
    """
    metadata["modified_time"] = str(datetime.datetime.now())

    return metadata


def save_to_version_file(versions, metadata):
    """
    Updates metadata and writes all to version file
    """
    metadata = update_metadata(metadata)

    new_version_file = {
        "metadata": metadata,
        "versions": versions
    }

    with open(VERSION_FILE, "wb") as version_file:
        pickle.dump(new_version_file, version_file)


def read_version_file():
    """
    Creates an empty version file if necessary
    """
    if not os.path.isfile(VERSION_FILE):
        new_version_contents = {
            "metadata": {
                "modified_time": str(datetime.datetime.now()),
            },
            "versions": {}
        }
        with open(VERSION_FILE, "wb") as version_file:
            pickle.dump(new_version_contents, version_file)
        return new_version_contents

    with open(VERSION_FILE, "rb") as version_file:
        versions = pickle.loads(version_file.read())

    return versions


def increment_version(version, increment):
    """
    Increments the given version by patch, minor, or major
    Version in format: major.minor.patch
    """
    version_nums = [int(val) for val in version.split(".")]

    if increment == "patch":
        version_nums[2] += 1
    elif increment == "minor":
        version_nums[1] += 1
    elif increment == "major":
        version_nums[0] += 1

    return ".".join([str(val) for val in version_nums])


def main():
    """
    Performs the specified action on the service in the versions file
    """
    parser = ArgumentParser(description='Versioning for services')

    initialize_arguments(parser)
    args = parser.parse_args()
    if not validate_arguments(args):
        raise Exception("Invalid arguments")

    version_file = read_version_file()
    versions = version_file["versions"]
    metadata = version_file["metadata"]

    if args.service not in versions:
        versions[args.service] = "0.0.0"

    if args.action == "get":
        version = versions[args.service]
    elif args.action == "patch":
        version = increment_version(versions[args.service], "patch")
    elif args.action == "minor":
        version = increment_version(versions[args.service], "minor")
    elif args.action == "major":
        version = increment_version(versions[args.service], "major")
    elif args.action == "get_last_modified_time":
        return metadata["modified_time"]

    versions[args.service] = version

    save_to_version_file(versions, metadata)

    return versions[args.service]


if __name__ == "__main__":
    print(main())
