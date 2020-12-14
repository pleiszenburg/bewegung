# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/vector/single3d.py: Single 3D Vector

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
from typing import Tuple, Type, Union

try:
    import numpy as np
    from numpy import ndarray
except ModuleNotFoundError:
    np, ndarray = None, None
from typeguard import typechecked

from ..abc import Dtype, PyNumber, PyNumber3D, Vector3DABC
from ..const import FLOAT_DEFAULT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Vector3D(Vector3DABC):
    """
    A single vector in 3D space.

    Mutable.

    Args:
        x : x component. Must have the same type like ``y`` and ``z``.
        y : y component. Must have the same type like ``x`` and ``z``.
        z : z component. Must have the same type like ``x`` and ``y``.
        dtype : Data type. Derived from ``x``, ``y`` and ``z`` if not explicitly provided.
    """

    _rad2deg = math.pi / 180.0
    _halfpi = math.pi / 2.0

    def __init__(self, x: PyNumber, y: PyNumber, z: PyNumber, dtype: Union[Type, None] = None):

        assert type(x) == type(y) == type(z)
        if dtype is None:
            dtype = type(x)
        else:
            assert dtype == type(x)

        self._x, self._y, self._z, self._dtype = x, y, z, dtype

    def __repr__(self) -> str:
        """
        String representation for interactive use
        """

        if self._dtype == int:
            return f'<Vector3D x={self._x:d} y={self._y:d} z={self._z:d} dtype={self._dtype.__name__:s}>'
        return f'<Vector3D x={self._x:e} y={self._y:e} z={self._z:e} dtype={self._dtype.__name__:s}>'

    def __eq__(self, other: Vector3DABC) -> bool:
        """
        Equality check between vectors

        Args:
            other : Another vector
        """

        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __mod__(self, other: Vector3DABC) -> bool:
        """
        Is-close check (relevant for dtype ``float``) between vectors

        Args:
            other : Another vector
        """

        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y) and math.isclose(self.z, other.z)

    def __add__(self, other: Vector3DABC) -> Vector3DABC:
        """
        Add operation between vectors

        Args:
            other : Another vector
        """

        return type(self)(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3DABC) -> Vector3DABC:
        """
        Substract operator between vectors

        Args:
            other : Another vector
        """

        return type(self)(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: PyNumber) -> Vector3DABC:
        """
        Multiplication with scalar

        Args:
            other : A number
        """

        return type(self)(self._x * other, self._y * other, self._z * other)

    def mul(self, scalar: PyNumber):
        """
        In-place multiplication with scalar

        Args:
            scalar : Vector is multiplied with this number.
        """

        self._x *= scalar
        self._y *= scalar
        self._z *= scalar
        assert type(self._x) == type(self._y) == type(self._z)
        self._dtype = type(self._x)

    def __matmul__(self, other: Vector3DABC) -> PyNumber:
        """
        Scalar product between vectors

        Args:
            other : Another vector
        """

        return self.x * other.x + self.y * other.y + self.z * other.z

    def as_dtype(self, dtype: Type) -> Vector3DABC:
        """
        Generates new vector with desired data type and returns it.

        Args:
            dtype : Desired data type of new vector
        """

        if dtype == self._dtype:
            return self.copy()
        return type(self)(dtype(self._x), dtype(self._y), dtype(self._z), dtype)

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> ndarray:
        """
        Exports vector as a ``numpy.ndarry`` object, shape ``(3,)``.

        Args:
            dtype : Desired ``numpy`` data type of new vector
        """

        if np is None:
            raise NotImplementedError('numpy is not available')
        return np.array(self.as_tuple(), dtype = dtype)

    def as_polar_tuple(self) -> Tuple[float, float, float]:
        """
        Exports vector as a tuple of polar coordinates
        """

        return (
            self.mag,
            math.acos(self._z / self.mag),
            math.atan2(self._y, self._x),
            )

    def as_tuple(self) -> PyNumber3D:
        """
        Exports vector as a tuple
        """

        return (self._x, self._y, self._z)

    def copy(self) -> Vector3DABC:
        """
        Copies vector
        """

        return type(self)(self._x, self._y, self._z, self._dtype)

    def update(self, x: PyNumber, y: PyNumber, z: PyNumber):
        """
        Updates vector components

        Args:
            x : x component. Must have the same type like ``y`` and ``z``.
            y : y component. Must have the same type like ``x`` and ``z``.
            z : z component. Must have the same type like ``x`` and ``y``.
        """

        assert type(x) == type(y) == type(z)
        self._x, self._y, self._z = x, y, z
        self._dtype = type(self._x)

    def update_from_vector(self, other: Vector3DABC):
        """
        Updates vector components with data from another vector

        Args:
            other : Another vector. Remains unchanged.
        """

        assert type(other.x) == type(other.y) == type(other.z)
        self._x, self._y, self._z = other.x, other.y, other.z
        self._dtype = type(self._x)

    @property
    def mag(self) -> float:
        """
        The vector's magnitude, computed on demand
        """

        return math.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

    @property
    def x(self) -> PyNumber:
        """
        x component
        """

        return self._x

    @x.setter
    def x(self, value: PyNumber):
        """
        x component
        """

        assert isinstance(value, self._dtype)
        self._x = value

    @property
    def y(self) -> PyNumber:
        """
        y component
        """

        return self._y

    @y.setter
    def y(self, value: PyNumber):
        """
        y component
        """

        assert isinstance(value, self._dtype)
        self._y = value

    @property
    def z(self) -> PyNumber:
        """
        z component
        """

        return self._z

    @z.setter
    def z(self, value: PyNumber):
        """
        z component
        """

        assert isinstance(value, self._dtype)
        self._z = value

    @property
    def dtype(self) -> Type:
        """
        (Python) data type of vector components
        """

        return self._dtype

    @classmethod
    def from_polar(cls, radius: PyNumber, theta: PyNumber, phi: PyNumber) -> Vector3DABC:
        """
        Generates vector object from polar coordinates

        Args:
            radius : A radius
            theta : An angle in radians
            phi : An angle in radians
        """

        RadiusSinTheta = radius * math.sin(theta)
        return cls(
            x = RadiusSinTheta * math.cos(phi),
            y = RadiusSinTheta * math.sin(phi),
            z = radius * math.cos(theta),
            )

    @classmethod
    def from_geographic(cls, radius: PyNumber, lon: PyNumber, lat: PyNumber) -> Vector3DABC:
        """
        Generates vector object from geographic polar coordinates

        Args:
            radius : A radius
            lon : An angle in degree
            lat : An angle in degree
        """

        return cls.from_polar(
            radius = radius,
            theta = cls._halfpi - (lat * cls._rad2deg),
            phi = lon * cls._rad2deg,
            )
