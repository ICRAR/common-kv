#
#  ICRAR - International Centre for Radio Astronomy Research
#  UWA - The University of Western Australia
#
#  Copyright (c) 2022.
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
from os import listdir
from os.path import join, exists, isdir, isfile
from typing import Union


def get_model_path(models: str, version: Union[str, int]) -> str:
    if version != "latest" and isinstance(version, int):
        model_path = join(models, f"version_{version}", "checkpoint")
        if exists(model_path) and isdir(model_path):
            checkpoints = [
                f
                for f in listdir(model_path)
                if isfile(join(model_path, f)) and f.endswith(".ckpt")
            ]
            if len(checkpoints) == 1:
                return join(model_path, checkpoints[0])
            elif len(checkpoints) > 1:
                raise NotImplementedError(
                    f"Not implemented: search for the latest checkpoint from the {len(checkpoints)} checkpoints"
                )

    # Find the latest
    max_version = -1
    versions = [
        f
        for f in listdir(models)
        if isdir(join(models, f)) and f.startswith("version_")
    ]
    for version in versions:
        elements = version.split("_")
        number = int(elements[1])
        if number > max_version:
            max_version = number

    model_path = join(models, f"version_{max_version}", "checkpoints")
    checkpoints = [
        f
        for f in listdir(model_path)
        if isfile(join(model_path, f)) and f.endswith(".ckpt")
    ]
    if len(checkpoints) == 1:
        return join(model_path, checkpoints[0])
    elif len(checkpoints) > 1:
        raise NotImplementedError(
            f"Not implemented: search for the latest checkpoint from the {len(checkpoints)} checkpoints"
        )
