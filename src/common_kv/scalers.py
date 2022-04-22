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
from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass
class FlatMinMaxScalerValues:
    feature_range: Tuple[float, float]
    minimum: float
    scale_factor: float


class FlatMinMaxScaler:
    """
    Scales the data as required
        X_std = (X - X.min()) / (X.max() - X.min())
        X_scaled = X_std * (max - min) + min
    """

    def __init__(self, feature_range=None, scaler_values=None):
        if feature_range is None and scaler_values is None:
            raise ValueError("Either feature_range or scaler_values must be specified")
        if feature_range is not None and scaler_values is not None:
            raise ValueError(
                "Only one of feature_range or scaler_values can be specified"
            )

        if scaler_values is not None:
            self._feature_range = scaler_values.feature_range
            self._minimum = scaler_values.minimum
            self._scale_factor = scaler_values.scale_factor
        else:
            self._feature_range = feature_range
            self._minimum = None
            self._scale_factor = None

    def fit(self, *arrays):
        data_min = None
        data_max = None
        for index, array_ in enumerate(arrays):
            if np.isnan(array_).any():
                raise ValueError(f"Array {index + 1} contains NaN(s)")

            if data_min is None:
                data_min = np.min(array_)
            else:
                data_min = min(data_min, np.min(array_))

            if data_max is None:
                data_max = np.max(array_)
            else:
                data_max = max(data_max, np.max(array_))

        data_range = data_max - data_min
        self._scale_factor = (
            self._feature_range[1] - self._feature_range[0]
        ) / data_range
        self._minimum = self._feature_range[0] - data_min * self._scale_factor

        return self

    def transform(self, array):
        x = array * self._scale_factor
        x += self._minimum
        return np.clip(x, self._feature_range[0], self._feature_range[1])

    def inverse_transform(self, array):
        x = array - self._minimum
        x /= self._scale_factor
        return x

    def scaler_values(self):
        return FlatMinMaxScalerValues(
            self._feature_range, self._minimum, self._scale_factor
        )
