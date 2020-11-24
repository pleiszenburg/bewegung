# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/vector/single2d.py: Single 2D Vector

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

from ..abc import Dtype, PyNumber, PyNumber2D, Vector2DABC
from ..const import FLOAT_DEFAULT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Vector2D(Vector2DABC):
    """
    Mutable
    """

    def __init__(self, x: PyNumber, y: PyNumber, dtype: Union[Type, None] = None):

        assert type(x) == type(y)
        if dtype is None:
            dtype = type(x)
        else:
            assert dtype == type(x)

        self._x, self._y, self._dtype = x, y, dtype

    def __repr__(self) -> str:
        if self._dtype == int:
            return f'<Vector2D x={self._x:d} y={self._y:d} dtype={self._dtype.__name__:s}>'
        return f'<Vector2D x={self._x:e} y={self._y:e} dtype={self._dtype.__name__:s}>'

    def __eq__(self, other: Vector2DABC) -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def __mod__(self, other: Vector2DABC) -> bool:
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __add__(self, other: Vector2DABC) -> Vector2DABC:
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2DABC) -> Vector2DABC:
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other: PyNumber) -> Vector2DABC:
        return type(self)(self._x * other, self._y * other)

    def mul(self, scalar: PyNumber):
        self._x *= scalar
        self._y *= scalar
        assert type(self._x) == type(self._y)
        self._dtype = type(self._x)

    def __matmul__(self, other: Vector2DABC) -> PyNumber:
        return self.x * other.x + self.y * other.y

    def as_dtype(self, dtype: Type) -> Vector2DABC:
        if dtype == self._dtype:
            return self.copy()
        return type(self)(dtype(self._x), dtype(self._y), dtype)

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> ndarray:
        if np is None:
            raise NotImplementedError('numpy is not available')
        return np.array(self.as_tuple(), dtype = dtype)

    def as_polar_tuple(self) -> Tuple[float, float]:
        return self.mag, math.atan2(self._y, self._x)

    def as_tuple(self) -> PyNumber2D:
        return self._x, self._y

    def copy(self) -> Vector2DABC:
        return type(self)(self._x, self._y, self._dtype)

    def update(self, x: PyNumber, y: PyNumber):
        assert type(x) == type(y)
        self._x, self._y = x, y
        self._dtype = type(self._x)

    def update_from_vector(self, other: Vector2DABC):
        assert type(other.x) == type(other.y)
        self._x, self._y = other.x, other.y
        self._dtype = type(self._x)

    @property
    def mag(self) -> float:
        return math.sqrt(self._x ** 2 + self._y ** 2)

    @property
    def x(self) -> PyNumber:
        return self._x
    @x.setter
    def x(self, value: PyNumber):
        assert isinstance(value, self._dtype)
        self._x = value

    @property
    def y(self) -> PyNumber:
        return self._y
    @y.setter
    def y(self, value: PyNumber):
        assert isinstance(value, self._dtype)
        self._y = value

    @property
    def dtype(self) -> Type:
        return self._dtype

    @classmethod
    def from_polar(cls, radius: PyNumber, angle: PyNumber) -> Vector2DABC:
        return cls(
            x = radius * math.cos(angle),
            y = radius * math.sin(angle),
            )
