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
import numpy as np
import pytest

from common_kv.scalers import FlatMinMaxScaler, FlatMinMaxScalerValues


@pytest.mark.parametrize(
    "fit_data, test_data, expected, feature_scale, minimum, scale_factor",
    [
        (
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[0, 0.2, 0.4], [0.6, 0.8, 1]], dtype=np.float32),
                (0, 1),
                -0.2,
                0.2,
        ),
        (
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[5.0, 6.0, 7.0], [8.0, 9.0, 10.0]], dtype=np.float32),
                (5, 10),
                4.0,
                1,
        ),
        (
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[-1, -0.8, -0.6], [-0.4, -0.2, 0]], dtype=np.float32),
                (-1, 0),
                -1.2,
                0.2,
        ),
        (
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[-20, -16, -12], [-8, -4, 0]], dtype=np.float32),
                (-20, 0),
                -24.0,
                4.0,
        ),
        (
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[1, 2, 3], [3, 2, 1]], dtype=np.float32),
                np.array([[0, 0.2, 0.4], [0.4, 0.2, 0]], dtype=np.float32),
                (0, 1),
                -0.2,
                0.2,
        ),
        (
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[1, 2, 3], [3, 2, 1]], dtype=np.float32),
                np.array([[5.0, 6.0, 7.0], [7.0, 6.0, 5.0]], dtype=np.float32),
                (5, 10),
                4.0,
                1,
        ),
        (
                (
                        np.array([[1, 2, 3]], dtype=np.float32),
                        np.array([[4, 5, 6]], dtype=np.float32),
                ),
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[0, 0.2, 0.4], [0.6, 0.8, 1]], dtype=np.float32),
                (0, 1),
                -0.2,
                0.2,
        ),
    ],
)
def test_min_max_scaler(
        fit_data, test_data, expected, feature_scale, minimum, scale_factor
):
    scaler = FlatMinMaxScaler(feature_scale)
    scaler.fit(fit_data)
    result = scaler.transform(test_data)
    scaler_values = scaler.scaler_values()

    assert np.allclose(result, expected)
    assert scaler_values.minimum == minimum
    assert scaler_values.scale_factor == scale_factor


@pytest.mark.parametrize(
    "expected, test_data, minimum, scale_factor",
    [
        (
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[0, 0.2, 0.4], [0.6, 0.8, 1]], dtype=np.float32),
                -0.2,
                0.2,
        ),
        (
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[5.0, 6.0, 7.0], [8.0, 9.0, 10.0]], dtype=np.float32),
                4.0,
                1,
        ),
        (
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[-1, -0.8, -0.6], [-0.4, -0.2, 0]], dtype=np.float32),
                -1.2,
                0.2,
        ),
        (
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[-20, -16, -12], [-8, -4, 0]], dtype=np.float32),
                -24.0,
                4.0,
        ),
        (
                np.array([[1, 2, 3], [3, 2, 1]], dtype=np.float32),
                np.array([[0, 0.2, 0.4], [0.4, 0.2, 0]], dtype=np.float32),
                -0.2,
                0.2,
        ),
        (
                np.array([[1, 2, 3], [3, 2, 1]], dtype=np.float32),
                np.array([[5.0, 6.0, 7.0], [7.0, 6.0, 5.0]], dtype=np.float32),
                4.0,
                1,
        ),
        (
                np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32),
                np.array([[0, 0.2, 0.4], [0.6, 0.8, 1]], dtype=np.float32),
                -0.2,
                0.2,
        ),
    ],
)
def test_inverse_min_max_scaler(expected, test_data, minimum, scale_factor):
    scaler = FlatMinMaxScaler(
        FlatMinMaxScalerValues(
            feature_range=(0, 1), minimum=minimum, scale_factor=scale_factor
        )
    )
    result = scaler.inverse_transform(test_data)

    assert np.allclose(result, expected)

