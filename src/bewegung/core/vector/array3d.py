# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/vector/array3d.py: 3D Vector Array

    Copyright (C) 2020 Sebastian M. Ernst <ernst@pleiszenburg.de>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU Lesser General Public License
Version 2.1 ("LGPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
https://github.com/pleiszenburg/bewegung/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from typing import Tuple

import numpy as np
from typeguard import typechecked

from ..abc import Dtype, Number, VectorArray3DABC
from ..const import FLOAT_DEFAULT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class VectorArray3D(VectorArray3DABC):

    def __init__(self, x: np.ndarray, y: np.ndarray, z: np.ndarray):
        assert x.ndim == 1
        assert y.ndim == 1
        assert z.ndim == 1
        assert x.shape[0] == y.shape[0] == z.shape[0]
        assert x.dtype == y.dtype == z.dtype
        self._x, self._y, self._z = x, y, z

    def __len__(self) -> int:
        return self._x.shape[0]

    def __eq__(self, other: VectorArray3DABC) -> bool:
        return np.array_equal(self.x, other.x) and np.array_equal(self.y, other.y) and np.array_equal(self.z, other.z)

    def __mod__(self, other: VectorArray3DABC) -> bool:
        return np.allclose(self.x, other.x) and np.allclose(self.y, other.y) and np.allclose(self.z, other.z)

    def __add__(self, other: VectorArray3DABC) -> VectorArray3DABC:
        assert len(self) == len(other)
        assert self.dtype == other.dtype
        return VectorArray3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: VectorArray3DABC) -> VectorArray3DABC:
        assert len(self) == len(other)
        assert self.dtype == other.dtype
        return VectorArray3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Number):
        return VectorArray3D(self._x * other, self._y * other, self._z * other)

    def mul(self, scalar: Number):
        np.multiply(self._x, scalar, out = self._x)
        np.multiply(self._y, scalar, out = self._y)
        np.multiply(self._z, scalar, out = self._z)

    def __matmul__(self, other: VectorArray3DABC) -> np.ndarray:
        assert len(self) == len(other)
        assert self.dtype == other.dtype
        return self.x * other.x + self.y * other.y + self.z * other.z

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> np.ndarray:
        a = np.zeros((len(self), 3), dtype = self.dtype)
        a[:, 0], a[:, 1], a[:, 2] = self._x, self._y, self._z
        return a if a.dtype == np.dtype(dtype) else a.astype(dtype)

    def as_polar_tuple(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        return (
            self.mag,
            np.acos(self._z / self.mag),
            np.atan2(self._y, self._x),
            )

    def as_tuple(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        return self._x.copy(), self._y.copy(), self._z.copy()

    def as_type(self, dtype: Dtype) -> VectorArray3DABC:
        return self.copy() if self.dtype == np.dtype(dtype) else VectorArray3D(
            self._x.astype(dtype), self._y.astype(dtype), self._z.astype(dtype),
        )

    def copy(self):
        return VectorArray3D(self._x.copy(), self._y.copy(), self._z.copy())

    # def update(self, x: float, y: float, z: float):
    #     self._x, self._y, self._z = x, y, z

    def update_from_vector(self, other: VectorArray3DABC):
        self._x[:], self._y[:], self._z[:] = other.x[:], other.y[:], other.z[:]

    @property
    def dtype(self) -> np.dtype:
        return self._x.dtype

    @property
    def mag(self) -> np.ndarray:
        return np.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

    @property
    def x(self) -> np.ndarray:
        return self._x
    # @x.setter
    # def x(self, value: float):
    #     self._x = value

    @property
    def y(self) -> np.ndarray:
        return self._y
    # @y.setter
    # def y(self, value: float):
    #     self._y = value

    @property
    def z(self) -> np.ndarray:
        return self._z
    # @z.setter
    # def z(self, value: float):
    #     self._z = value

    @classmethod
    def from_polar(cls, radius: np.ndarray, theta: np.ndarray, phi: np.ndarray) -> VectorArray3DABC:
        assert radius.ndim == 1
        assert theta.ndim == 1
        assert phi.ndim == 1
        assert radius.shape[0] == theta.shape[0] == phi.shape[0]
        assert radius.dtype == theta.dtype == phi.dtype
        RadiusSinTheta = radius * np.sin(theta)
        return cls(
            x = RadiusSinTheta * np.cos(phi),
            y = RadiusSinTheta * np.sin(phi),
            z = radius * np.cos(theta),
            )

    @classmethod
    def from_geographic(cls, radius: np.ndarray, lon: np.ndarray, lat: np.ndarray) -> VectorArray3DABC:
        assert radius.ndim == 1
        assert lon.ndim == 1
        assert lat.ndim == 1
        assert radius.shape[0] == lon.shape[0] == lat.shape[0]
        assert radius.dtype == lon.dtype == lat.dtype
        rad2deg = np.dtype(radius.dtype).type(np.pi / 180.0)
        halfpi = np.dtype(radius.dtype).type(np.pi / 2.0)
        return cls.from_polar(
            radius = radius,
            theta = halfpi - (lat * rad2deg),
            phi = lon * rad2deg,
            )
