# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/vector.py: Vector algebra

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

import math
import typing

import numpy as np
from typeguard import typechecked

from .abc import Vector2DABC, Vector3DABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Vector2D(Vector2DABC):
    def __init__(self, x: float, y: float):
        self._x, self._y = x, y
    def __eq__(self, other: Vector2DABC) -> bool:
        return (self.x == other.x) and (self.y == other.y)
    def __mod__(self, other: Vector2DABC) -> bool:
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
    def __add__(self, other: Vector2DABC) -> Vector2DABC:
        return Vector2D(self.x + other.x, self.y + other.y)
    def __sub__(self, other: Vector2DABC) -> Vector2DABC:
        return Vector2D(self.x - other.x, self.y - other.y)
    def __mul__(self, other: float):
        return Vector2D(self._x * other, self._y * other)
    def mul(self, scalar: float):
        self._x *= scalar
        self._y *= scalar
    def __matmul__(self, other: Vector2DABC) -> float:
        return self.x * other.x + self.y * other.y
    def as_ndarray(self, dtype: str = 'f4') -> np.ndarray:
        return np.array(self.as_tuple(), dtype = dtype)
    def as_polar_tuple(self) -> typing.Tuple[float, float]:
        return self.mag, math.atan2(self._y, self._x)
    def as_tuple(self) -> typing.Tuple[float, float]:
        return self._x, self._y
    def copy(self):
        return Vector2D(self._x, self._y)
    def update(self, x: float, y: float):
        self._x, self._y = x, y
    def update_from_vector(self, other: Vector2DABC):
        self._x, self._y = other.x, other.y
    @property
    def mag(self) -> float:
        return math.sqrt(self._x ** 2 + self._y ** 2)
    @property
    def x(self) -> float:
        return self._x
    @x.setter
    def x(self, value: float):
        self._x = value
    @property
    def y(self) -> float:
        return self._y
    @y.setter
    def y(self, value: float):
        self._y = value
    @classmethod
    def from_polar(cls, radius: float, angle: float) -> Vector2DABC:
        return cls(
            x = radius * math.cos(angle),
            y = radius * math.sin(angle),
            )

@typechecked
class Vector3D(Vector3DABC):
    _rad2deg = math.pi / 180.0
    _halfpi = math.pi / 2.0
    def __init__(self, x: float, y: float, z: float):
        self._x, self._y, self._z = x, y, z
    def __eq__(self, other: Vector3DABC) -> bool:
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
    def __mod__(self, other: Vector3DABC) -> bool:
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y) and math.isclose(self.z, other.z)
    def __add__(self, other: Vector3DABC) -> Vector3DABC:
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other: Vector3DABC) -> Vector3DABC:
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    def __mul__(self, other: float):
        return Vector3D(self._x * other, self._y * other, self._z * other)
    def mul(self, scalar: float):
        self._x *= scalar
        self._y *= scalar
        self._z *= scalar
    def __matmul__(self, other: Vector3DABC) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z
    def as_ndarray(self, dtype: str = 'f4') -> np.ndarray:
        return np.array(self.as_tuple(), dtype = dtype)
    def as_polar_tuple(self) -> typing.Tuple[float, float, float]:
        return (
            self.mag,
            math.acos(self._z / self.mag),
            math.atan2(self._y, self._x),
            )
    def as_tuple(self) -> typing.Tuple[float, float, float]:
        return (self._x, self._y, self._z)
    def copy(self):
        return Vector3D(self._x, self._y, self._z)
    def update(self, x: float, y: float, z: float):
        self._x, self._y, self._z = x, y, z
    def update_from_vector(self, other: Vector3DABC):
        self._x, self._y, self._z = other.x, other.y, other.z
    @property
    def mag(self) -> float:
        return math.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)
    @property
    def x(self) -> float:
        return self._x
    @x.setter
    def x(self, value: float):
        self._x = value
    @property
    def y(self) -> float:
        return self._y
    @y.setter
    def y(self, value: float):
        self._y = value
    @property
    def z(self) -> float:
        return self._z
    @z.setter
    def z(self, value: float):
        self._z = value
    @classmethod
    def from_polar(cls, radius: float, theta: float, phi: float) -> Vector3DABC:
        RadiusSinTheta = radius * math.sin(theta)
        return cls(
            x = RadiusSinTheta * math.cos(phi),
            y = RadiusSinTheta * math.sin(phi),
            z = radius * math.cos(theta),
            )
    @classmethod
    def from_geographic(cls, radius: float, lon: float, lat: float) -> Vector3DABC:
        return cls.from_polar(
            radius = radius,
            theta = cls._halfpi - (lat * cls._rad2deg),
            phi = lon * cls._rad2deg,
            )
