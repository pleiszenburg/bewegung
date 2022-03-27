# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/_single2d.py: Single 2D Vector

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
    Number2D,
    NumberType,
    Vector2DABC,
)
from ._const import FLOAT_DEFAULT
from ._lib import dtype_name
from ._numpy import np, ndarray
from ._single import Vector
from ._svg import Svg

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Vector2D(Vector, Vector2DABC):
    """
    A single vector in 2D space.

    Mutable.

    Args:
        x : x component. Must have the same type like ``y``.
        y : y component. Must have the same type like ``x``.
        dtype : Data type. Derived from ``x`` and ``y`` if not explicitly provided.
        meta : A dict holding arbitrary metadata.
    """

    def __init__(self, x: Number, y: Number, dtype: Union[NumberType, None] = None, meta: Union[MetaDict, None] = None):

        if dtype is None:
            if type(x) != type(y):
                raise TypeError('can not guess dtype - inconsistent')
        else:
            x, y = dtype(x), dtype(y)

        self._x, self._y = x, y
        super().__init__(meta = meta)

    def __repr__(self) -> str:
        """
        String representation for interactive use
        """

        if self.dtype == int:
            return f'<Vector2D x={self._x:d} y={self._y:d} dtype={dtype_name(self.dtype):s}>'
        return f'<Vector2D x={self._x:e} y={self._y:e} dtype={dtype_name(self.dtype):s}>'

    def _repr_svg_(self) -> str:

        return Svg(self).render()

    def __eq__(self, other: Any) -> Union[bool, NotImplementedType]:
        """
        Equality check between vectors

        Args:
            other : Another vector
        """

        if not isinstance(other, Vector2DABC):
            return NotImplemented

        return bool(self.x == other.x) and bool(self.y == other.y)

    def __mod__(self, other: Any) -> Union[bool, NotImplementedType]:
        """
        Is-close check (relevant for dtype ``float``) between vectors

        Args:
            other : Another vector
        """

        if not isinstance(other, Vector2DABC):
            return NotImplemented

        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __add__(self, other: Any) -> Union[Vector2DABC, NotImplementedType]:
        """
        Add operation between vectors or a vector and a vector array

        Args:
            other : Another vector
        """

        if not isinstance(other, Vector2DABC):
            return NotImplemented

        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Any) -> Union[Vector2DABC, NotImplementedType]:
        """
        Substract operator between vectors or a vector and a vector array

        Args:
            other : Another vector
        """

        if not isinstance(other, Vector2DABC):
            return NotImplemented

        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Any) -> Union[Vector2DABC, NotImplementedType]:
        """
        Multiplication with scalar

        Args:
            other : A number
        """

        if not isinstance(other, Number):
            return NotImplemented

        return type(self)(self._x * other, self._y * other)

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

        assert type(self._x) == type(self._y) # very unlikely

    def __matmul__(self, other: Any) -> Union[Number, NotImplementedType]:
        """
        Scalar product between vectors

        Args:
            other : Another vector
        """

        if not isinstance(other, Vector2DABC):
            return NotImplemented

        return self.x * other.x + self.y * other.y

    def as_dtype(self, dtype: NumberType) -> Vector2DABC:
        """
        Generates new vector with desired data type and returns it.

        Args:
            dtype : Desired data type of new vector
        """

        if dtype == self.dtype:
            return self.copy()
        return type(self)(dtype(self._x), dtype(self._y), dtype)

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> ndarray:
        """
        Exports vector as a ``numpy.ndarry`` object, shape ``(2,)``.

        Args:
            dtype : Desired ``numpy`` data type of new vector
        """

        if np is None:
            raise NotImplementedError('numpy is not available')
        return np.array(self.as_tuple(), dtype = dtype)

    def as_polar_tuple(self) -> Tuple[float, float]:
        """
        Exports vector as a tuple of polar coordinates
        """

        return self.mag, self.angle

    def as_tuple(self) -> Number2D:
        """
        Exports vector as a tuple
        """

        return self._x, self._y

    def copy(self) -> Vector2DABC:
        """
        Copies vector & meta data
        """

        return type(self)(x = self._x, y = self._y, dtype = self.dtype, meta = self._meta.copy())

    def update(self, x: Number, y: Number):
        """
        Updates vector components

        Args:
            x : x component. Must have the same type like ``y``.
            y : y component. Must have the same type like ``x``.
        """

        if type(x) != type(y):
            raise TypeError('inconsistent dtype')

        self._x, self._y = x, y

    def update_from_vector(self, other: Vector2DABC):
        """
        Updates vector components with data from another vector

        Args:
            other : Another vector. Remains unchanged.
        """

        self._x, self._y = other.x, other.y

    @property
    def mag(self) -> float:
        """
        The vector's magnitude, computed on demand
        """

        return math.sqrt(self._x ** 2 + self._y ** 2)

    @property
    def angle(self) -> float:
        """
        The vector's angle in radians, computed on demand
        """

        return math.atan2(self._y, self._x)

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

        return 2

    @classmethod
    def from_polar(cls, radius: Number, angle: Number, meta: Union[MetaDict, None] = None) -> Vector2DABC:
        """
        Generates vector object from polar coordinates

        Args:
            radius : A radius
            angle : An angle in radians
            meta : A dict holding arbitrary metadata
        """

        return cls(
            x = radius * math.cos(angle),
            y = radius * math.sin(angle),
            meta = meta,
            )
