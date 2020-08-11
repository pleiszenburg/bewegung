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
from typing import Tuple

import numpy as np
from typeguard import typechecked

from ..abc import Dtype, Vector2DABC
from ..const import FLOAT_DEFAULT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Vector2D(Vector2DABC):
    """
    Mutable
    """

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

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> np.ndarray:
        return np.array(self.as_tuple(), dtype = dtype)

    def as_polar_tuple(self) -> Tuple[float, float]:
        return self.mag, math.atan2(self._y, self._x)

    def as_tuple(self) -> Tuple[float, float]:
        return self._x, self._y

    def copy(self) -> Vector2DABC:
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
