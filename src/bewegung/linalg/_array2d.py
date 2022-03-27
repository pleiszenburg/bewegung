# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/_array2d.py: 2D Vector Array

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

from numbers import Number
from typing import Any, List, Tuple, Union

from ..lib import typechecked
from ._abc import (
    Dtype,
    Iterable,
    MetaArrayDict,
    NotImplementedType,
    VectorArray2DABC,
)
from ._array import VectorArray
from ._const import FLOAT_DEFAULT
from ._lib import dtype_np2py, dtype_name
from ._numpy import np
from ._single2d import Vector2D

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class VectorArray2D(VectorArray, VectorArray2DABC):
    """
    An array of vectors in 2D space.

    Mutable.

    Args:
        x : x components. Must have the same dtype like ``y``.
        y : y components. Must have the same dtype like ``x``.
        meta : A dict holding arbitrary metadata.
    """

    def __init__(self, x: np.ndarray, y: np.ndarray, dtype: Union[Dtype, None] = None, meta: Union[MetaArrayDict, None] = None):

        if x.ndim != 1:
            raise ValueError('inconsistent: x.ndim != 1')
        if y.ndim != 1:
            raise ValueError('inconsistent: x.ndim != 1')
        if x.shape[0] != y.shape[0]:
            raise ValueError('inconsistent length')

        if dtype is None:
            if x.dtype != y.dtype:
                raise TypeError('can not guess dtype - inconsistent')
        else:
            x = x if x.dtype == np.dtype(dtype) else x.astype(dtype)
            y = y if y.dtype == np.dtype(dtype) else y.astype(dtype)

        self._x, self._y = x, y
        self._iterstate = 0
        super().__init__(meta = meta)

    def __repr__(self) -> str:
        """
        String representation for interactive use
        """

        return f'<VectorArray2D len={len(self):d} dtype={dtype_name(self.dtype):s}>'

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
            return Vector2D(
                x = dtype(self._x[idx]),
                y = dtype(self._y[idx]),
                dtype = dtype,
                meta = {key: value[idx] for key, value in self._meta.items()},
            )

        return VectorArray2D(
            x = self._x[idx].copy(),
            y = self._y[idx].copy(),
            meta = {key: value[idx].copy() for key, value in self._meta.items()},
        )

    def __iter__(self) -> VectorArray2DABC:
        """
        Iterator interface (1/2)
        """

        self._iterstate = 0
        return self

    def __next__(self) -> Vector2D:
        """
        Iterator interface (2/2)
        """

        if self._iterstate == len(self):
            self._iterstate = 0 # reset
            raise StopIteration()

        value = self[self._iterstate]
        self._iterstate += 1 # increment
        return value

    def __eq__(self, other: Any) -> Union[bool, NotImplementedType]:
        """
        Equality check between vector arrays

        Args:
            other : Another vector array of equal length
        """

        if not isinstance(other, VectorArray2DABC):
            return NotImplemented

        return np.array_equal(self.x, other.x) and np.array_equal(self.y, other.y)

    def __mod__(self, other: Any) -> Union[bool, NotImplementedType]:
        """
        Is-close check between vector arrays

        Args:
            other : Another vector array of equal length
        """

        if not isinstance(other, VectorArray2DABC):
            return NotImplemented

        return np.allclose(self.x, other.x) and np.allclose(self.y, other.y)

    def __add__(self, other: Any) -> Union[VectorArray2DABC, NotImplementedType]:
        """
        Add operation between vector arrays or a vector array and a vector

        Args:
            other : Another vector array of equal length
        """

        if not any(isinstance(other, t) for t in (VectorArray2DABC, Vector2D)):
            return NotImplemented

        if isinstance(other, VectorArray2DABC):
            if len(self) != len(other):
                raise ValueError('inconsistent length')
            if self.dtype != other.dtype:
                raise TypeError('inconsistent dtype')

        return VectorArray2D(self.x + other.x, self.y + other.y)

    def __radd__(self, *args, **kwargs):

        return self.__add__(*args, **kwargs)

    def __sub__(self, other: Any) -> Union[VectorArray2DABC, NotImplementedType]:
        """
        Substract operator between vector arrays or a vector array and a vector

        Args:
            other : Another vector array of equal length
        """

        if not any(isinstance(other, t) for t in (VectorArray2DABC, Vector2D)):
            return NotImplemented

        if isinstance(other, VectorArray2DABC):
            if len(self) != len(other):
                raise ValueError('inconsistent length')
            if self.dtype != other.dtype:
                raise TypeError('inconsistent dtype')

        return VectorArray2D(self.x - other.x, self.y - other.y)

    def __rsub__(self, *args, **kwargs):

        return self.__sub__(*args, **kwargs)

    def __mul__(self, other: Any) -> Union[VectorArray2DABC, NotImplementedType]:
        """
        Multiplication with scalar

        Args:
            other : A number
        """

        if not isinstance(other, Number):
            return NotImplemented

        return VectorArray2D(self._x * other, self._y * other)

    def __rmul__(self, *args, **kwargs):

        return self.__mul__(*args, **kwargs)

    def mul(self, scalar: Number):
        """
        In-place multiplication with scalar

        Args:
            scalar : Vector array is multiplied with this number.
        """

        np.multiply(self._x, scalar, out = self._x)
        np.multiply(self._y, scalar, out = self._y)

    def __matmul__(self, other: Any) -> Union[np.ndarray, NotImplementedType]:
        """
        Scalar product between vector arrays

        Args:
            other : Another vector array of equal length
        """

        if not isinstance(other, VectorArray2DABC):
            return NotImplemented

        if len(self) != len(other):
            raise ValueError('inconsistent length')
        if self.dtype != other.dtype:
            raise TypeError('inconsistent dtype')

        return self.x * other.x + self.y * other.y

    def as_list(self) -> List[Vector2D]:
        """
        Exports a list of :class:`bewegung.Vector2D` objects
        """

        return list(self)

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

        return self.mag, self.angle

    def as_tuple(self, copy: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Exports vector array as a tuple of vector components in ``numpy.ndarry`` objects

        Args:
            copy : Provide a copy of underlying ``numpy.ndarry``
        """

        if copy:
            return self._x.copy(), self._y.copy()

        return self._x, self._y

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
        Copies vector array & meta data
        """

        return VectorArray2D(
            x = self._x.copy(),
            y = self._y.copy(),
            meta = {key: value.copy() for key, value in self._meta.items()},
        )

    def update_from_vectorarray(self, other: VectorArray2DABC):
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
    def ndim(self) -> int:
        """
        Number of dimensions
        """

        return 2

    @property
    def mag(self) -> np.ndarray:
        """
        The vectors' magnitudes, computed on demand
        """

        return np.sqrt(self._x ** 2 + self._y ** 2)

    @property
    def angle(self) -> np.ndarray:
        """
        The vectors' angles in radians, computed on demand
        """

        return np.arctan2(self._y, self._x)

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
    def from_iterable(cls, obj: Iterable[Vector2D], dtype: Dtype = FLOAT_DEFAULT) -> VectorArray2DABC:
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
        keys = set()
        for idx, item in enumerate(obj):
            x[idx], y[idx] = item.x, item.y
            keys.update(item.meta.keys())

        meta = {
            key: np.array([item.meta.get(key) for item in obj])
            for key in keys
        }

        return cls(x = x, y = y, meta = meta,)

    @classmethod
    def from_polar(cls, radius: np.ndarray, angle: np.ndarray, meta: Union[MetaArrayDict, None] = None) -> VectorArray2DABC:
        """
        Generates vector array object from arrays of polar vector components

        Args:
            radius : Radius components
            angle : Angle components in radians
            meta : A dict holding arbitrary metadata
        """

        if radius.ndim != 1:
            raise ValueError('inconsistent: radius.ndim != 1')
        if angle.ndim != 1:
            raise ValueError('inconsistent: angle.ndim != 1')
        if radius.shape[0] != angle.shape[0]:
            raise ValueError('inconsistent shape')
        if radius.dtype != angle.dtype:
            raise ValueError('inconsistent dtype')

        x, y = np.cos(angle), np.sin(angle)
        np.multiply(x, radius, out = x)
        np.multiply(y, radius, out = y)

        return cls(x = x, y = y, meta = meta,)
