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

from typing import List, Tuple, Union

import numpy as np
from typeguard import typechecked

from .lib import dtype_np2py
from .single3d import Vector3D
from ..abc import Dtype, Number, VectorArray3DABC, VectorIterable3D
from ..const import FLOAT_DEFAULT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class VectorArray3D(VectorArray3DABC):
    """
    An array of vectors in 3D space.

    Mutable.

    Args:
        x : x components. Must have the same dtype like ``y`` and ``z``.
        y : y components. Must have the same dtype like ``x`` and ``z``.
        z : z components. Must have the same dtype like ``x`` and ``y``.
    """


    def __init__(self, x: np.ndarray, y: np.ndarray, z: np.ndarray):

        assert x.ndim == 1
        assert y.ndim == 1
        assert z.ndim == 1
        assert x.shape[0] == y.shape[0] == z.shape[0]
        assert x.dtype == y.dtype == z.dtype
        self._x, self._y, self._z = x, y, z

    def __repr__(self) -> str:
        """
        String representation for interactive use
        """

        return f'<VectorArray3D len={len(self):d}>'

    def __len__(self) -> int:
        """
        Length of array
        """

        return self._x.shape[0]

    def __getitem__(self, idx: Union[int, slice]) -> Union[Vector3D, VectorArray3DABC]:
        """
        Item access, returning an independent object - either
        a :class:`bewegung.Vector3D` (index access) or
        a :class:`bewegung.VectorArray§D` (slicing)

        Args:
            idx : Either an index or a slice
        """

        if isinstance(idx, int):
            dtype = dtype_np2py(self.dtype)
            return Vector3D(dtype(self._x[idx]), dtype(self._y[idx]), dtype(self._z[idx]), dtype = dtype)

        return VectorArray3D(self._x[idx].copy(), self._y[idx].copy(), self._z[idx].copy())

    def __eq__(self, other: VectorArray3DABC) -> bool:
        """
        Equality check between vector arrays

        Args:
            other : Another vector array of equal length
        """

        return np.array_equal(self.x, other.x) and np.array_equal(self.y, other.y) and np.array_equal(self.z, other.z)

    def __mod__(self, other: VectorArray3DABC) -> bool:
        """
        Is-close check between vector arrays

        Args:
            other : Another vector array of equal length
        """

        return np.allclose(self.x, other.x) and np.allclose(self.y, other.y) and np.allclose(self.z, other.z)

    def __add__(self, other: VectorArray3DABC) -> VectorArray3DABC:
        """
        Add operation between vector arrays

        Args:
            other : Another vector array of equal length
        """

        assert len(self) == len(other)
        assert self.dtype == other.dtype
        return VectorArray3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: VectorArray3DABC) -> VectorArray3DABC:
        """
        Substract operator between vector arrays

        Args:
            other : Another vector array of equal length
        """

        assert len(self) == len(other)
        assert self.dtype == other.dtype
        return VectorArray3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Number) -> VectorArray3DABC:
        """
        Multiplication with scalar

        Args:
            other : A number
        """

        return VectorArray3D(self._x * other, self._y * other, self._z * other)

    def mul(self, scalar: Number):
        """
        In-place multiplication with scalar

        Args:
            scalar : Vector array is multiplied with this number.
        """

        np.multiply(self._x, scalar, out = self._x)
        np.multiply(self._y, scalar, out = self._y)
        np.multiply(self._z, scalar, out = self._z)

    def __matmul__(self, other: VectorArray3DABC) -> np.ndarray:
        """
        Scalar product between vector arrays

        Args:
            other : Another vector array of equal length
        """

        assert len(self) == len(other)
        assert self.dtype == other.dtype
        return self.x * other.x + self.y * other.y + self.z * other.z

    def as_list(self) -> List[Vector3D]:
        """
        Exports a list of :class:`bewegung.Vector3D` objects
        """

        dtype = dtype_np2py(self.dtype)
        return [
            Vector3D(dtype(self._x[idx]), dtype(self._y[idx]), dtype(self._z[idx]), dtype = dtype)
            for idx in range(len(self))
        ]

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> np.ndarray:
        """
        Exports vector array as a ``numpy.ndarry`` object, shape ``(len(self), 3)``.

        Args:
            dtype : Desired ``numpy`` data type of new vector
        """

        a = np.zeros((len(self), 3), dtype = self.dtype)
        a[:, 0], a[:, 1], a[:, 2] = self._x, self._y, self._z
        return a if a.dtype == np.dtype(dtype) else a.astype(dtype)

    def as_polar_tuple(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Exports vector array as a tuple of polar vector components in ``numpy.ndarry`` objects
        """

        return (
            self.mag,
            np.arccos(self._z / self.mag),
            np.arctan2(self._y, self._x),
            )

    def as_tuple(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Exports vector array as a tuple of vector components in ``numpy.ndarry`` objects
        """

        return self._x.copy(), self._y.copy(), self._z.copy()

    def as_type(self, dtype: Dtype) -> VectorArray3DABC:
        """
        Exports vector array as another vector array with new dtype

        Args:
            dtype : Desired ``numpy`` data type of new vector array
        """

        return self.copy() if self.dtype == np.dtype(dtype) else VectorArray3D(
            self._x.astype(dtype), self._y.astype(dtype), self._z.astype(dtype),
        )

    def copy(self) -> VectorArray3DABC:
        """
        Copies vector array
        """

        return VectorArray3D(self._x.copy(), self._y.copy(), self._z.copy())

    def update_from_vector(self, other: VectorArray3DABC):
        """
        Updates vector components with data from another vector array

        Args:
            x : x components. Must have the same dtype like ``y`` and ``z``.
            y : y components. Must have the same dtype like ``x`` and ``z``.
            z : z components. Must have the same dtype like ``x`` and ``y``.
        """

        self._x[:], self._y[:], self._z[:] = other.x[:], other.y[:], other.z[:]

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

        return np.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

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

    @property
    def z(self) -> np.ndarray:
        """
        z components, mutable
        """

        return self._z

    @z.setter
    def z(self, value: float):
        ""
        raise NotImplementedError()

    @classmethod
    def from_iterable(cls, obj: VectorIterable3D, dtype: Dtype = FLOAT_DEFAULT) -> VectorArray3DABC:
        """
        Generates vector array object from an iterable of :class:`bewegung.Vector3D` objects

        Args:
            obj : iterable
            dtype : Desired ``numpy`` data type of new vector array
        """

        if not isinstance(obj, list):
            obj = list(obj)
        x = np.zeros((len(obj),), dtype = dtype)
        y = np.zeros((len(obj),), dtype = dtype)
        z = np.zeros((len(obj),), dtype = dtype)
        for idx, item in enumerate(obj):
            x[idx], y[idx], z[idx] = item.x, item.y, item.z
        return cls(x = x, y = y, z = z,)

    @classmethod
    def from_polar(cls, radius: np.ndarray, theta: np.ndarray, phi: np.ndarray) -> VectorArray3DABC:
        """
        Generates vector array object from arrays of polar vector components

        Args:
            radius : Radius components
            theta : Angle components in radians
            phi : Angle components in radians
        """

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
        """
        Generates vector array object from arrays of geographic polar vector components

        Args:
            radius : Radius components
            lon : Angle components in degree
            lat : Angle components in degree
        """

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
