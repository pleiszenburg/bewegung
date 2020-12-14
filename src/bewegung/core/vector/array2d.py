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

from typing import List, Tuple, Union

import numpy as np
from typeguard import typechecked

from .lib import dtype_np2py
from .single2d import Vector2D
from ..abc import Dtype, Number, VectorArray2DABC, VectorIterable2D
from ..const import FLOAT_DEFAULT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class VectorArray2D(VectorArray2DABC):
    """
    An array of vectors in 2D space.

    Mutable.

    Args:
        x : x components. Must have the same dtype like ``y``.
        y : y components. Must have the same dtype like ``x``.
    """

    def __init__(self, x: np.ndarray, y: np.ndarray):

        assert x.ndim == 1
        assert y.ndim == 1
        assert x.shape[0] == y.shape[0]
        assert x.dtype == y.dtype
        self._x, self._y = x, y

    def __repr__(self) -> str:
        """
        String representation for interactive use
        """

        return f'<VectorArray2D len={len(self):d}>'

    def __len__(self) -> int:
        """
        Length of array
        """

        return self._x.shape[0]

    def __getitem__(self, idx: Union[int, slice]) -> Union[Vector2D, VectorArray2DABC]:
        """
        Item access, returning an independent object - either
        a :class:`bewegung.Vector2D` (index access) or
        a :class:`bewegung.VectorArray2D` (slicing)

        Args:
            idx : Either an index or a slice
        """

        if isinstance(idx, int):
            dtype = dtype_np2py(self.dtype)
            return Vector2D(dtype(self._x[idx]), dtype(self._y[idx]), dtype = dtype)

        return VectorArray2D(self._x[idx].copy(), self._y[idx].copy())

    def __eq__(self, other: VectorArray2DABC) -> bool:
        """
        Equality check between vector arrays

        Args:
            other : Another vector array of equal length
        """

        return np.array_equal(self.x, other.x) and np.array_equal(self.y, other.y)

    def __mod__(self, other: VectorArray2DABC) -> bool:
        """
        Is-close check between vector arrays

        Args:
            other : Another vector array of equal length
        """

        return np.allclose(self.x, other.x) and np.allclose(self.y, other.y)

    def __add__(self, other: VectorArray2DABC) -> VectorArray2DABC:
        """
        Add operation between vector arrays

        Args:
            other : Another vector array of equal length
        """

        assert len(self) == len(other)
        assert self.dtype == other.dtype
        return VectorArray2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: VectorArray2DABC) -> VectorArray2DABC:
        """
        Substract operator between vector arrays

        Args:
            other : Another vector array of equal length
        """

        assert len(self) == len(other)
        assert self.dtype == other.dtype
        return VectorArray2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Number) -> VectorArray2DABC:
        """
        Multiplication with scalar

        Args:
            other : A number
        """

        return VectorArray2D(self._x * other, self._y * other)

    def mul(self, scalar: Number):
        """
        In-place multiplication with scalar

        Args:
            scalar : Vector array is multiplied with this number.
        """

        np.multiply(self._x, scalar, out = self._x)
        np.multiply(self._y, scalar, out = self._y)

    def __matmul__(self, other: VectorArray2DABC) -> np.ndarray:
        """
        Scalar product between vector arrays

        Args:
            other : Another vector array of equal length
        """

        assert len(self) == len(other)
        assert self.dtype == other.dtype
        return self.x * other.x + self.y * other.y

    def as_list(self) -> List[Vector2D]:
        """
        Exports a list of :class:`bewegung.Vector2D` objects
        """

        dtype = dtype_np2py(self.dtype)
        return [
            Vector2D(dtype(self._x[idx]), dtype(self._y[idx]), dtype = dtype)
            for idx in range(len(self))
        ]

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> np.ndarray:
        """
        Exports vector array as a ``numpy.ndarry`` object, shape ``(len(self), 2)``.

        Args:
            dtype : Desired ``numpy`` data type of new vector
        """

        a = np.zeros((len(self), 2), dtype = self.dtype)
        a[:, 0], a[:, 1] = self._x, self._y
        return a if a.dtype == np.dtype(dtype) else a.astype(dtype)

    def as_polar_tuple(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Exports vector array as a tuple of polar vector components in ``numpy.ndarry`` objects
        """

        return self.mag, np.arctan2(self._y, self._x)

    def as_tuple(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Exports vector array as a tuple of vector components in ``numpy.ndarry`` objects
        """

        return self._x.copy(), self._y.copy()

    def as_type(self, dtype: Dtype) -> VectorArray2DABC:
        """
        Exports vector array as another vector array with new dtype

        Args:
            dtype : Desired ``numpy`` data type of new vector array
        """

        return self.copy() if self.dtype == np.dtype(dtype) else VectorArray2D(
            self._x.astype(dtype), self._y.astype(dtype),
        )

    def copy(self) -> VectorArray2DABC:
        """
        Copies vector array
        """

        return VectorArray2D(self._x.copy(), self._y.copy())

    def update_from_vector(self, other: VectorArray2DABC):
        """
        Updates vector components with data from another vector array

        Args:
            x : x components. Must have the same dtype like ``y``.
            y : y components. Must have the same dtype like ``x``.
        """

        self._x[:], self._y[:] = other.x[:], other.y[:]

    @property
    def dtype(self) -> np.dtype:
        """
        (``numpy``) data type of vector array components
        """

        return self._x.dtype

    @property
    def mag(self) -> np.ndarray:
        """
        The vectors' magnitudes, computed on demand
        """

        return np.sqrt(self._x ** 2 + self._y ** 2)

    @property
    def x(self) -> np.ndarray:
        """
        x components, mutable
        """

        return self._x

    @x.setter
    def x(self, value: float):
        ""
        raise NotImplementedError()

    @property
    def y(self) -> np.ndarray:
        """
        y components, mutable
        """

        return self._y

    @y.setter
    def y(self, value: float):
        ""
        raise NotImplementedError()

    @classmethod
    def from_iterable(cls, obj: VectorIterable2D, dtype: Dtype = FLOAT_DEFAULT) -> VectorArray2DABC:
        """
        Generates vector array object from an iterable of :class:`bewegung.Vector2D` objects

        Args:
            obj : iterable
            dtype : Desired ``numpy`` data type of new vector array
        """

        if not isinstance(obj, list):
            obj = list(obj)
        x = np.zeros((len(obj),), dtype = dtype)
        y = np.zeros((len(obj),), dtype = dtype)
        for idx, item in enumerate(obj):
            x[idx], y[idx] = item.x, item.y
        return cls(x = x, y = y,)

    @classmethod
    def from_polar(cls, radius: np.ndarray, angle: np.ndarray) -> VectorArray2DABC:
        """
        Generates vector array object from arrays of polar vector components

        Args:
            radius : Radius components
            angle : Angle components in radians
        """

        assert radius.ndim == 1
        assert angle.ndim == 1
        assert radius.shape[0] == angle.shape[0]
        assert radius.dtype == angle.dtype
        x, y = np.cos(angle), np.sin(angle)
        np.multiply(x, radius, out = x)
        np.multiply(y, radius, out = y)
        return cls(x = x, y = y,)
