# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/_array3d.py: 3D Vector Array

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
    VectorArray3DABC,
)
from ._array import VectorArray
from ._const import FLOAT_DEFAULT
from ._lib import dtype_np2py, dtype_name
from ._numpy import np
from ._single3d import Vector3D

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class VectorArray3D(VectorArray, VectorArray3DABC):
    """
    An array of vectors in 3D space.

    Mutable.

    Args:
        x : x components. Must have the same dtype like ``y`` and ``z``.
        y : y components. Must have the same dtype like ``x`` and ``z``.
        z : z components. Must have the same dtype like ``x`` and ``y``.
        meta : A dict holding arbitrary metadata.
    """

    def __init__(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, dtype: Union[Dtype, None] = None, meta: Union[MetaArrayDict, None] = None):

        if x.ndim != 1:
            raise ValueError('inconsistent: x.ndim != 1')
        if y.ndim != 1:
            raise ValueError('inconsistent: x.ndim != 1')
        if z.ndim != 1:
            raise ValueError('inconsistent: z.ndim != 1')
        if not x.shape[0] == y.shape[0] == z.shape[0]:
            raise ValueError('inconsistent length')

        if dtype is None:
            if x.dtype != y.dtype:
                raise TypeError('can not guess dtype - inconsistent')
        else:
            x = x if x.dtype == np.dtype(dtype) else x.astype(dtype)
            y = y if y.dtype == np.dtype(dtype) else y.astype(dtype)
            z = z if z.dtype == np.dtype(dtype) else z.astype(dtype)

        self._x, self._y, self._z = x, y, z
        self._iterstate = 0
        super().__init__(meta = meta)

    def __repr__(self) -> str:
        """
        String representation for interactive use
        """

        return f'<VectorArray3D len={len(self):d} dtype={dtype_name(self.dtype):s}>'

    def __len__(self) -> int:
        """
        Length of array
        """

        return self._x.shape[0]

    def __getitem__(self, idx: Union[int, slice]) -> Union[Vector3D, VectorArray3DABC]:
        """
        Item access, returning an independent object - either
        a :class:`bewegung.Vector3D` (index access) or
        a :class:`bewegung.VectorArray3D` (slicing)

        Args:
            idx : Either an index or a slice
        """

        if isinstance(idx, int):
            dtype = dtype_np2py(self.dtype)
            return Vector3D(
                x = dtype(self._x[idx]),
                y = dtype(self._y[idx]),
                z = dtype(self._z[idx]),
                dtype = dtype,
                meta = {key: value[idx] for key, value in self._meta.items()},
            )

        return VectorArray3D(
            x = self._x[idx].copy(),
            y = self._y[idx].copy(),
            z = self._z[idx].copy(),
            meta = {key: value[idx].copy() for key, value in self._meta.items()},
        )

    def __iter__(self) -> VectorArray3DABC:
        """
        Iterator interface (1/2)
        """

        self._iterstate = 0
        return self

    def __next__(self) -> Vector3D:
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

        if not isinstance(other, VectorArray3DABC):
            return NotImplemented

        return np.array_equal(self.x, other.x) and np.array_equal(self.y, other.y) and np.array_equal(self.z, other.z)

    def __mod__(self, other: Any) -> Union[bool, NotImplementedType]:
        """
        Is-close check between vector arrays

        Args:
            other : Another vector array of equal length
        """

        if not isinstance(other, VectorArray3DABC):
            return NotImplemented

        return np.allclose(self.x, other.x) and np.allclose(self.y, other.y) and np.allclose(self.z, other.z)

    def __add__(self, other: Any) -> Union[VectorArray3DABC, NotImplementedType]:
        """
        Add operation between vector arrays or a vector array and a vector

        Args:
            other : Another vector array of equal length
        """

        if not any(isinstance(other, t) for t in (VectorArray3DABC, Vector3D)):
            return NotImplemented

        if isinstance(other, VectorArray3DABC):
            if len(self) != len(other):
                raise ValueError('inconsistent length')
            if self.dtype != other.dtype:
                raise TypeError('inconsistent dtype')

        return VectorArray3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __radd__(self, *args, **kwargs):

        return self.__add__(*args, **kwargs)

    def __sub__(self, other: Any) -> Union[VectorArray3DABC, NotImplementedType]:
        """
        Substract operator between vector arrays or a vector array and a vector

        Args:
            other : Another vector array of equal length
        """

        if not any(isinstance(other, t) for t in (VectorArray3DABC, Vector3D)):
            return NotImplemented

        if isinstance(other, VectorArray3DABC):
            if len(self) != len(other):
                raise ValueError('inconsistent length')
            if self.dtype != other.dtype:
                raise TypeError('inconsistent dtype')

        return VectorArray3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rsub__(self, *args, **kwargs):

        return self.__sub__(*args, **kwargs)

    def __mul__(self, other: Any) -> Union[VectorArray3DABC, NotImplementedType]:
        """
        Multiplication with scalar

        Args:
            other : A number
        """

        if not isinstance(other, Number):
            return NotImplemented

        return VectorArray3D(self._x * other, self._y * other, self._z * other)

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
        np.multiply(self._z, scalar, out = self._z)

    def __matmul__(self, other: Any) -> Union[np.ndarray, NotImplementedType]:
        """
        Scalar product between vector arrays

        Args:
            other : Another vector array of equal length
        """

        if not isinstance(other, VectorArray3DABC):
            return NotImplemented

        if len(self) != len(other):
            raise ValueError('inconsistent length')
        if self.dtype != other.dtype:
            raise TypeError('inconsistent dtype')

        return self.x * other.x + self.y * other.y + self.z * other.z

    def as_list(self) -> List[Vector3D]:
        """
        Exports a list of :class:`bewegung.Vector3D` objects
        """

        return list(self)

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

        return (self.mag, self.theta, self.phi)

    def as_geographic_tuple(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Exports vector array as a tuple of geographic coordinate components
        in ``numpy.ndarry`` objects (radius, lon, lat)
        """

        return (self.mag, self.lon, self.lat)

    def as_tuple(self, copy: bool = True) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Exports vector array as a tuple of vector components in ``numpy.ndarry`` objects

        Args:
            copy : Provide a copy of underlying ``numpy.ndarry``
        """

        if copy:
            return self._x.copy(), self._y.copy(), self._z.copy()

        return self._x, self._y, self._z

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
        Copies vector array & meta data
        """

        return VectorArray3D(
            x = self._x.copy(),
            y = self._y.copy(),
            z = self._z.copy(),
            meta = {key: value.copy() for key, value in self._meta.items()},
        )

    def update_from_vectorarray(self, other: VectorArray3DABC):
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
    def ndim(self) -> int:
        """
        Number of dimensions
        """

        return 3

    @property
    def mag(self) -> np.ndarray:
        """
        The vectors' magnitudes, computed on demand
        """

        return np.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

    @property
    def theta(self) -> np.ndarray:
        """
        The vectors' thetas in radians, computed on demand
        """

        return np.arccos(self._z / self.mag)

    @property
    def phi(self) -> np.ndarray:
        """
        The vectors' phis in radians, computed on demand
        """

        return np.arctan2(self._y, self._x)

    @property
    def lat(self) -> float:
        """
        The vectors' geographic latitude in degree, computed on demand
        """

        rad2deg = self.dtype.type(180.0 / np.pi)
        halfpi = self.dtype.type(np.pi / 2.0)

        return -(self.theta - halfpi) * rad2deg

    @property
    def lon(self) -> float:
        """
        The vectors' gepgraphic longitude in degree, computed on demand
        """

        rad2deg = self.dtype.type(180.0 / np.pi)

        return self.phi * rad2deg

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
    def from_iterable(cls, obj: Iterable[Vector3D], dtype: Dtype = FLOAT_DEFAULT) -> VectorArray3DABC:
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
        keys = set()
        for idx, item in enumerate(obj):
            x[idx], y[idx], z[idx] = item.x, item.y, item.z
            keys.update(item.meta.keys())

        meta = {
            key: np.array([item.meta.get(key) for item in obj])
            for key in keys
        }

        return cls(x = x, y = y, z = z, meta = meta,)

    @classmethod
    def from_polar(cls, radius: np.ndarray, theta: np.ndarray, phi: np.ndarray, meta: Union[MetaArrayDict, None] = None) -> VectorArray3DABC:
        """
        Generates vector array object from arrays of polar vector components

        Args:
            radius : Radius components
            theta : Angle components in radians
            phi : Angle components in radians
            meta : A dict holding arbitrary metadata
        """

        if radius.ndim != 1:
            raise ValueError('inconsistent: radius.ndim != 1')
        if theta.ndim != 1:
            raise ValueError('inconsistent: theta.ndim != 1')
        if phi.ndim != 1:
            raise ValueError('inconsistent: phi.ndim != 1')
        if not radius.shape[0] == theta.shape[0] == phi.shape[0]:
            raise ValueError('inconsistent shape')
        if not radius.dtype == theta.dtype == phi.dtype:
            raise ValueError('inconsistent dtype')

        RadiusSinTheta = radius * np.sin(theta)
        return cls(
            x = RadiusSinTheta * np.cos(phi),
            y = RadiusSinTheta * np.sin(phi),
            z = radius * np.cos(theta),
            meta = meta,
            )

    @classmethod
    def from_geographic(cls, radius: np.ndarray, lon: np.ndarray, lat: np.ndarray, meta: Union[MetaArrayDict, None] = None) -> VectorArray3DABC:
        """
        Generates vector array object from arrays of geographic polar vector components

        Args:
            radius : Radius components
            lon : Angle components in degree
            lat : Angle components in degree
            meta : A dict holding arbitrary metadata
        """

        if radius.ndim != 1:
            raise ValueError('inconsistent: radius.ndim != 1')
        if lon.ndim != 1:
            raise ValueError('inconsistent: lon.ndim != 1')
        if lat.ndim != 1:
            raise ValueError('inconsistent: lat.ndim != 1')
        if not radius.shape[0] == lon.shape[0] == lat.shape[0]:
            raise ValueError('inconsistent shape')
        if not radius.dtype == lon.dtype == lat.dtype:
            raise ValueError('inconsistent dtype')

        deg2rad = np.dtype(radius.dtype).type(np.pi / 180.0)
        halfpi = np.dtype(radius.dtype).type(np.pi / 2.0)
        return cls.from_polar(
            radius = radius,
            theta = halfpi - (lat * deg2rad),
            phi = lon * deg2rad,
            meta = meta,
            )
