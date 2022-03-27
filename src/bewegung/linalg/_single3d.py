# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/_single3d.py: Single 3D Vector

    Copyright (C) 2020-2022 Sebastian M. Ernst <ernst@pleiszenburg.de>

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
from numbers import Number
from typing import Any, Tuple, Union

from ..lib import typechecked
from ._abc import (
    Dtype,
    NotImplementedType,
    MetaDict,
    Number3D,
    NumberType,
    Vector3DABC,
)
from ._const import FLOAT_DEFAULT
from ._lib import dtype_name
from ._numpy import np, ndarray
from ._single import Vector

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Vector3D(Vector, Vector3DABC):
    """
    A single vector in 3D space.

    Mutable.

    Args:
        x : x component. Must have the same type like ``y`` and ``z``.
        y : y component. Must have the same type like ``x`` and ``z``.
        z : z component. Must have the same type like ``x`` and ``y``.
        dtype : Data type. Derived from ``x``, ``y`` and ``z`` if not explicitly provided.
        meta : A dict holding arbitrary metadata.
    """

    _deg2rad = math.pi / 180.0
    _rad2deg = 1.0 / _deg2rad
    _halfpi = math.pi / 2.0

    def __init__(self, x: Number, y: Number, z: Number, dtype: Union[NumberType, None] = None, meta: Union[MetaDict, None] = None):

        if dtype is None:
            if not type(x) == type(y) == type(z):
                raise TypeError('can not guess dtype - inconsistent')
        else:
            x, y, z = dtype(x), dtype(y), dtype(z)

        self._x, self._y, self._z = x, y, z
        super().__init__(meta = meta)

    def __repr__(self) -> str:
        """
        String representation for interactive use
        """

        if self.dtype == int:
            return f'<Vector3D x={self._x:d} y={self._y:d} z={self._z:d} dtype={dtype_name(self.dtype):s}>'
        return f'<Vector3D x={self._x:e} y={self._y:e} z={self._z:e} dtype={dtype_name(self.dtype):s}>'

    def __eq__(self, other: Any) -> Union[bool, NotImplementedType]:
        """
        Equality check between vectors

        Args:
            other : Another vector
        """

        if not isinstance(other, Vector3DABC):
            return NotImplemented

        return bool(self.x == other.x) and bool(self.y == other.y) and bool(self.z == other.z)

    def __mod__(self, other: Any) -> Union[bool, NotImplementedType]:
        """
        Is-close check (relevant for dtype ``float``) between vectors

        Args:
            other : Another vector
        """

        if not isinstance(other, Vector3DABC):
            return NotImplemented

        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y) and math.isclose(self.z, other.z)

    def __add__(self, other: Any) -> Union[Vector3DABC, NotImplementedType]:
        """
        Add operation between vectors or a vector and a vector array

        Args:
            other : Another vector
        """

        if not isinstance(other, Vector3DABC):
            return NotImplemented

        return type(self)(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Any) -> Union[Vector3DABC, NotImplementedType]:
        """
        Substract operator between vectors or a vector and a vector array

        Args:
            other : Another vector
        """

        if not isinstance(other, Vector3DABC):
            return NotImplemented

        return type(self)(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Any) -> Union[Vector3DABC, NotImplementedType]:
        """
        Multiplication with scalar

        Args:
            other : A number
        """

        if not isinstance(other, Number):
            return NotImplemented

        return type(self)(self._x * other, self._y * other, self._z * other)

    def __rmul__(self, *args, **kwargs):

        return self.__mul__(*args, **kwargs)

    def mul(self, scalar: Number):
        """
        In-place multiplication with scalar

        Args:
            scalar : Vector is multiplied with this number.
        """

        self._x *= scalar
        self._y *= scalar
        self._z *= scalar

        assert type(self._x) == type(self._y) == type(self._z) # very unlikely

    def __matmul__(self, other: Any) -> Union[Number, NotImplementedType]:
        """
        Scalar product between vectors

        Args:
            other : Another vector
        """

        if not isinstance(other, Vector3DABC):
            return NotImplemented

        return self.x * other.x + self.y * other.y + self.z * other.z

    def as_dtype(self, dtype: NumberType) -> Vector3DABC:
        """
        Generates new vector with desired data type and returns it.

        Args:
            dtype : Desired data type of new vector
        """

        if dtype == self.dtype:
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

        return (self.mag, self.theta, self.phi)

    def as_geographic_tuple(self) -> Tuple[float, float, float]:
        """
        Exports vector as a tuple of geographic coordinates (radius, lon, lat)
        """

        return (self.mag, self.lon, self.lat)

    def as_tuple(self) -> Number3D:
        """
        Exports vector as a tuple
        """

        return (self._x, self._y, self._z)

    def copy(self) -> Vector3DABC:
        """
        Copies vector & meta data
        """

        return type(self)(x = self._x, y = self._y, z = self._z, dtype = self.dtype, meta = self._meta.copy())

    def update(self, x: Number, y: Number, z: Number):
        """
        Updates vector components

        Args:
            x : x component. Must have the same type like ``y`` and ``z``.
            y : y component. Must have the same type like ``x`` and ``z``.
            z : z component. Must have the same type like ``x`` and ``y``.
        """

        if not type(x) == type(y) == type(z):
            raise TypeError('inconsistent dtype')

        self._x, self._y, self._z = x, y, z

    def update_from_vector(self, other: Vector3DABC):
        """
        Updates vector components with data from another vector

        Args:
            other : Another vector. Remains unchanged.
        """

        self._x, self._y, self._z = other.x, other.y, other.z

    @property
    def mag(self) -> float:
        """
        The vector's magnitude, computed on demand
        """

        return math.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

    @property
    def theta(self) -> float:
        """
        The vector's theta in radians, computed on demand
        """

        return math.acos(self._z / self.mag)

    @property
    def phi(self) -> float:
        """
        The vector's phi in radians, computed on demand
        """

        return math.atan2(self._y, self._x)

    @property
    def lat(self) -> float:
        """
        The vector's geographic latitude in degree, computed on demand
        """

        return -(self.theta - self._halfpi) * self._rad2deg

    @property
    def lon(self) -> float:
        """
        The vector's gepgraphic longitude in degree, computed on demand
        """

        return self.phi * self._rad2deg

    @property
    def x(self) -> Number:
        """
        x component
        """

        return self._x

    @x.setter
    def x(self, value: Number):
        """
        x component
        """

        if not isinstance(value, self.dtype):
            raise TypeError('inconsistent dtype')

        self._x = value

    @property
    def y(self) -> Number:
        """
        y component
        """

        return self._y

    @y.setter
    def y(self, value: Number):
        """
        y component
        """

        if not isinstance(value, self.dtype):
            raise TypeError('inconsistent dtype')

        self._y = value

    @property
    def z(self) -> Number:
        """
        z component
        """

        return self._z

    @z.setter
    def z(self, value: Number):
        """
        z component
        """

        if not isinstance(value, self.dtype):
            raise TypeError('inconsistent dtype')

        self._z = value

    @property
    def dtype(self) -> NumberType:
        """
        (Python) data type of vector components
        """

        return type(self._x)

    @property
    def ndim(self) -> int:
        """
        Number of dimensions
        """

        return 3

    @classmethod
    def from_polar(cls, radius: Number, theta: Number, phi: Number, meta: Union[MetaDict, None] = None) -> Vector3DABC:
        """
        Generates vector object from polar coordinates

        Args:
            radius : A radius
            theta : An angle in radians
            phi : An angle in radians
            meta : A dict holding arbitrary metadata
        """

        RadiusSinTheta = radius * math.sin(theta)
        return cls(
            x = RadiusSinTheta * math.cos(phi),
            y = RadiusSinTheta * math.sin(phi),
            z = radius * math.cos(theta),
            meta = meta,
            )

    @classmethod
    def from_geographic(cls, radius: Number, lon: Number, lat: Number, meta: Union[MetaDict, None] = None) -> Vector3DABC:
        """
        Generates vector object from geographic polar coordinates

        Args:
            radius : A radius
            lon : An angle in degree
            lat : An angle in degree
            meta : A dict holding arbitrary metadata
        """

        return cls.from_polar(
            radius = radius,
            theta = cls._halfpi - (lat * cls._deg2rad),
            phi = lon * cls._deg2rad,
            meta = meta,
            )
