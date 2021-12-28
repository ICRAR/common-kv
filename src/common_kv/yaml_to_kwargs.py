#
#  ICRAR - International Centre for Radio Astronomy Research
#  UWA - The University of Western Australia
#
#  Copyright (c) 2021.
#  Copyright by UWA (in the framework of the ICRAR)
#  All rights reserved
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston,
#  MA 02111-1307  USA
#

from os.path import exists
from typing import Dict, List, Optional

from ruamel.yaml import YAML


def make_hierarchy(yaml_config) -> Dict:
    """

    Parameters
    ----------
    yaml_config
        The YAML data to be processed

    Returns
    -------
    Dict
        A dictionary of the data in the form
        {
            'key1/key2': blah1,
            'key1/key3': blah2
        }

    """
    dictionary = {}
    for key, value in yaml_config.items():
        if isinstance(value, Dict):
            dictionary[key] = child_dictionary = make_hierarchy(value)
            dictionary.update(
                {f"{key}/{key_}": value_ for key_, value_ in child_dictionary.items()}
            )
        else:
            dictionary[key] = value

    return dictionary


def read_yaml(yaml_file: str) -> Dict:
    """
    Read a yaml file and produce a dictionary of tags

    Parameters
    ----------
    yaml_file: str
        the yaml file to read

    Returns
    -------
    Dict
        A dictionary of the data in the form
        {
            'key1/key2': blah1,
            'key1/key3': blah2
        }

    """

    if not exists(yaml_file):
        raise FileNotFoundError(f"Could not find the file: {yaml_file}")

    with open(yaml_file, "r") as yaml_file:
        yaml = YAML()
        yaml_config = yaml.load(yaml_file)

    return make_hierarchy(yaml_config)


def check_keys(*args, **kwargs):
    """
    Check the keys exist.

    Throws a value exception if the key is missing

    Parameters
    ----------
    args
        all the keys to check
    kwargs
        the yaml dictionary

    Returns
    -------
        None
    """
    missing_keys = [key for key in args if key not in kwargs]
    if missing_keys:
        error_message = "\n  ".join(missing_keys)
        raise ValueError(f"The following keys are missing:\n  {error_message}")


def get_children(tag: str, **kwargs) -> Optional[List]:
    """
    Get the child of a tag

    Parameters
    ----------
    tag
        the tag to get the children of
    kwargs
        the tags to check

    Returns
    -------
        None if there are no tags
        A list of tags
    """
    # From the root tag
    if tag == "":
        return [key for key in kwargs.keys() if key.find("/") == -1]

    if tag not in kwargs or not isinstance(kwargs[tag], dict):
        return None

    return [key for key in kwargs[tag].keys() if key.find("/") == -1]
