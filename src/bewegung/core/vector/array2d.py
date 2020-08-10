# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/vector/array2d.py: 2D Vector Array

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

# from typing import Tuple

import numpy as np
from typeguard import typechecked

from ..abc import Dtype, Number, VectorArray2DABC
from ..const import FLOAT_DEFAULT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class VectorArray2D(VectorArray2DABC):

    def __init__(self, x: np.ndarray, y: np.ndarray):
        assert x.ndim == 1
        assert y.ndim == 1
        assert x.shape[0] == y.shape[0]
        assert x.dtype == y.dtype
        self._x, self._y = x, y

    def __len__(self) -> int:
        return self._x.shape[0]

    def __eq__(self, other: VectorArray2DABC) -> bool:
        return np.array_equal(self.x, other.x) and np.array_equal(self.y, other.y)

    def __mod__(self, other: VectorArray2DABC) -> bool:
        return np.allclose(self.x, other.x) and np.allclose(self.y, other.y)

    def __add__(self, other: VectorArray2DABC) -> VectorArray2DABC:
        assert len(self) == len(other)
        assert self.dtype == other.dtype
        return VectorArray2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: VectorArray2DABC) -> VectorArray2DABC:
        assert len(self) == len(other)
        assert self.dtype == other.dtype
        return VectorArray2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Number):
        return VectorArray2D(self._x * other, self._y * other)

    def mul(self, scalar: Number):
        np.multiply(self._x, scalar, out = self._x)
        np.multiply(self._y, scalar, out = self._y)

    def __matmul__(self, other: VectorArray2DABC) -> np.ndarray:
        assert len(self) == len(other)
        assert self.dtype == other.dtype
        return self.x * other.x + self.y * other.y

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> np.ndarray:
        a = np.zeros((len(self), 2), dtype = self.dtype)
        a[:, 0], a[:, 1] = self._x, self._y
        return a if a.dtype == np.dtype(dtype) else a.astype(dtype)

    # def as_polar_tuple(self) -> Tuple[float, float]:
    #     return self.mag, math.atan2(self._y, self._x)

    # def as_tuple(self) -> Tuple[float, float]:
    #     return self._x, self._y

    def as_type(self, dtype: Dtype) -> VectorArray2DABC:
        return self.copy() if self.dtype == np.dtype(dtype) else VectorArray2D(
            self._x.astype(dtype), self._y.astype(dtype),
        )

    def copy(self):
        return VectorArray2D(self._x.copy(), self._y.copy())

    # def update(self, x: float, y: float):
    #     self._x, self._y = x, y

    def update_from_vector(self, other: VectorArray2DABC):
        self._x[:], self._y[:] = other.x[:], other.y[:]

    @property
    def dtype(self) -> np.dtype:
        return self._x.dtype

    @property
    def mag(self) -> np.ndarray:
        return np.sqrt(self._x ** 2 + self._y ** 2)

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

    @classmethod
    def from_polar(cls, radius: np.ndarray, angle: np.ndarray) -> VectorArray2DABC:
        assert radius.ndim == 1
        assert angle.ndim == 1
        assert radius.shape[0] == angle.shape[0]
        assert radius.dtype == angle.dtype
        x, y = np.cos(angle), np.sin(angle)
        np.multiply(x, radius, out = x)
        np.multiply(y, radius, out = y)
        return cls(x = x, y = y,)