#
#    ICRAR - International Centre for Radio Astronomy Research
#    (c) UWA - The University of Western Australia, 2021
#    Copyright by UWA (in the framework of the ICRAR)
#    All rights reserved
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston,
#    MA 02111-1307  USA
#
from os.path import exists
from typing import Dict

from ruamel.yaml import YAML


def make_hierarchy(yaml_config) -> Dict:
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
    if not exists(yaml_file):
        raise FileNotFoundError(f"Could not find the file: {yaml_file}")

    with open(yaml_file, "r") as yaml_file:
        yaml = YAML()
        yaml_config = yaml.load(yaml_file)

    return make_hierarchy(yaml_config)


def check_keys(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    missing_keys = [key for key in args if key not in kwargs]
    if missing_keys:
        error_message = "\n  ".join(missing_keys)
        raise ValueError(f"The following keys are missing:\n  {error_message}")
