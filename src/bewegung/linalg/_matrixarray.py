# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/_matrixarray.py: Array of simple 2x2/3x3 matrices for rotations

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
    MatrixArrayABC,
    MetaArrayDict,
    NotImplementedType,
)
from ._const import FLOAT_DEFAULT
from ._array import VectorArray
from ._lib import dtype_np2py, dtype_name
from ._numpy import np, ndarray
from ._single import Vector
from ._single3d import Vector3D
from ._array2d import VectorArray2D
from ._array3d import VectorArray3D
from ._matrix import Matrix

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class MatrixArray(MatrixArrayABC):
    """
    An array implementation of simple matrices for transforming vectors and vector arrays

    Mutable.

    Args:
        matrix : 2D or 3D arrangement in a list of lists containing numpy nd arrays
    """

    def __init__(self, matrix = Iterable[Iterable[ndarray]], dtype: Union[Dtype, None] = None, meta: Union[MetaArrayDict, None] = None):

        matrix = [list(row) for row in matrix] # convert to lists or copy lists

        rows = len(matrix)
        if rows not in (2, 3): # allow 2D and 3D
            raise ValueError('dimension mismatch - neither 2D nor 3D')
        if not all((len(row) == rows for row in matrix)):
            raise ValueError('inconsistent rows')

        if not all(col.ndim == 1 for row in matrix for col in row):
            raise ValueError('inconsistent: ndarray.ndim != 1')

        length = matrix[0][0].shape[0]
        if not all(col.shape[0] == length for row in matrix for col in row):
            raise ValueError('inconsistent length')

        if dtype is None:
            dtype = matrix[0][0].dtype
            if not all(col.dtype == dtype for row in matrix for col in row):
                raise TypeError('can not guess dtype - inconsistent')
        else:
            dtype = np.dtype(dtype)
            matrix = [
                [
                    col if col.dtype == dtype else col.astype(dtype)
                    for col in row
                ]
                for row in matrix
            ]

        self._matrix = matrix
        self._iterstate = 0

        meta = {} if meta is None else dict(meta)

        if not all(value.ndim == 1 for value in meta.values()):
            raise ValueError('inconsistent: meta_value.ndim != 1')
        if not all(value.shape[0] == len(self) for value in meta.values()):
            raise ValueError('inconsistent length')

        self._meta = meta

    def __repr__(self) -> str:
        """
        String representation for interactive use
        """

        return f'<MatrixArray ndim={len(self._matrix):d} dtype={dtype_name(self.dtype):s} len={len(self):d}>'

    def __len__(self) -> int:
        """
        Length of array
        """

        return self._matrix[0][0].shape[0]

    def __matmul__(self, other: Any) -> Union[VectorArray, NotImplementedType]:
        """
        Multiplies the matrix array with a vector or array of vectors
        and returns the resulting new vector or array of vectors.
        Raises an exception if matrix and vector or
        array of vectors have different numbers of dimensions.

        Args:
            vector : A 2D or 3D vector or array of vectors
        """

        if not any(isinstance(other, t) for t in (Vector, VectorArray)):
            return NotImplemented

        if self.ndim != other.ndim:
            raise ValueError('dimension mismatch')

        if len(self) > 1 and isinstance(other, VectorArray):
            if len(other) > 1 and len(self) != len(other):
                raise ValueError('length mismatch')

        vector_tuple = other.as_tuple(copy = False) if isinstance(other, VectorArray) else other.as_tuple()

        values = [
            np.sum(np.array([
                matrix_element * vector_coordinate
                for matrix_element, vector_coordinate in zip(matrix_row, vector_tuple)
            ]), axis = 0)
            for matrix_row in self._matrix
        ]

        return VectorArray2D(*values) if len(vector_tuple) == 2 else VectorArray3D(*values)

    def __getitem__(self, idx: Union[int, slice]) -> Union[Matrix, MatrixArrayABC]:
        """
        Item access, returns value at position

        Args:
            index : Row, column and position index
        """

        if isinstance(idx, slice):
            return MatrixArray(
                matrix = [
                    [col[idx].copy() for col in row]
                    for row in self._matrix
                ],
                meta = {key: value[idx].copy() for key, value in self._meta.items()},
            )

        dtype = dtype_np2py(self.dtype)

        return Matrix(
            matrix = [
                [dtype(col[idx]) for col in row]
                for row in self._matrix
            ],
            meta = {key: value[idx] for key, value in self._meta.items()},
        )

    def __iter__(self) -> MatrixArrayABC:
        """
        Iterator interface (1/2)
        """

        self._iterstate = 0
        return self

    def __next__(self) -> Matrix:
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
        Equality check between matrix arrays

        Args:
            other : Another matrix array of equal length
        """

        if not isinstance(other, MatrixArrayABC):
            return NotImplemented

        if self.ndim != other.ndim or len(self) != len(other):
            return False

        return all(
            np.array_equal(self_col, other_col)
            for self_row, other_row in zip(self._matrix, other._matrix)
            for self_col, other_col in zip(self_row, other_row)
        )

    def __mod__(self, other: Any) -> Union[bool, NotImplementedType]:
        """
        Is-close check between matrix arrays

        Args:
            other : Another matrix array of equal length
        """

        if not isinstance(other, MatrixArrayABC):
            return NotImplemented

        if self.ndim != other.ndim or len(self) != len(other):
            return False

        return all(
            np.allclose(self_col, other_col)
            for self_row, other_row in zip(self._matrix, other._matrix)
            for self_col, other_col in zip(self_row, other_row)
        )

    def as_list(self) -> List[Matrix]:
        """
        Exports a list of :class:`bewegung.Matrix` objects
        """

        return list(self)

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> ndarray:
        """
        Exports matrix array as a ``numpy.ndarry`` object, shape ``(len(self), self.ndim, self.ndim)``.

        Args:
            dtype : Desired ``numpy`` data type of new vector
        """

        return np.moveaxis(np.array(self._matrix, dtype = dtype), 2, 0)

    def as_tuple(self, copy: bool = True) -> Tuple[Tuple[ndarray, ...], ...]:
        """
        Exports matrix array as a tuple of tuples of ``numpy.ndarray`` objects

        Args:
            copy : Provide a copy of underlying ``numpy.ndarry``
        """

        if copy:
            return tuple(tuple(col.copy() for col in row) for row in self._matrix)

        return tuple(tuple(col for col in row) for row in self._matrix)

    def as_type(self, dtype: Dtype) -> MatrixArrayABC:
        """
        Exports matrix array as another matrix array with new dtype

        Args:
            dtype : Desired ``numpy`` data type of new vector array
        """

        return self.copy() if self.dtype == np.dtype(dtype) else Matrix([
            [col.astype(dtype) for col in row] for row in self._matrix
        ])

    def copy(self) -> MatrixArrayABC:
        """
        Copies matrix array & meta data
        """

        return type(self)(
            matrix = [
                [col.copy() for col in row]
                for row in self._matrix
            ],
            meta = {key: value.copy() for key, value in self._meta.items()},
        )

    @property
    def dtype(self) -> np.dtype:
        """
        (Python) data type of matrix components
        """

        return self._matrix[0][0].dtype

    @property
    def ndim(self) -> int:
        """
        Number of dimensions, either ``2`` or ``3``.
        """

        return len(self._matrix)

    @property
    def meta(self) -> MetaArrayDict:
        """
        meta data dict
        """

        return self._meta

    @classmethod
    def from_iterable(cls, obj: Iterable[Matrix], dtype: Dtype = FLOAT_DEFAULT) -> MatrixArrayABC:
        """
        Generates matrix array object from an iterable of :class:`bewegung.Matrix` objects

        Args:
            obj : iterable
            dtype : Desired ``numpy`` data type of new vector array
        """

        if not isinstance(obj, list):
            obj = list(obj)

        ndim = obj[0].ndim
        if not all(item.ndim == ndim for item in obj):
            raise ValueError('inconsistent ndim')

        matrix = [
            [
                np.zeros((len(obj),), dtype = dtype)
                for __ in range(len(obj))
            ]
            for _ in range(len(obj))
        ]

        keys = set()
        for idx, item in enumerate(obj):
            for row in range(ndim):
                for col in range(ndim):
                    matrix[row][col][idx] = item[row][col]
            keys.update(item.meta.keys())

        meta = {
            key: np.array([item.meta.get(key) for item in obj])
            for key in keys
        }

        return cls(matrix = matrix, meta = meta,)

    @classmethod
    def from_ndarray(cls, matrix_array: ndarray, meta: Union[MetaArrayDict, None] = None) -> MatrixArrayABC:
        """
        Generates new matrix array object from single ``numpy.ndarray``
        object of shape ``(length, ndim, ndim)``

        Args:
            matrix_array : Input data
        """

        if matrix_array.ndim != 3:
            raise ValueError('dimension mismatch: ndim != 3)')
        if matrix_array.shape[1:] not in ((2, 2), (3, 3)):
            raise ValueError('dimension mismatch: not 2x2 or 3x3)')

        ndim = matrix_array.shape[1]

        return cls(
            matrix = [
                [matrix_array[:, row, col] for col in range(ndim)]
                for row in range(ndim)
            ],
            meta = meta,
        )

    @classmethod
    def from_2d_rotation(cls, a: ndarray, meta: Union[MetaArrayDict, None] = None) -> MatrixArrayABC:
        """
        Generates new 2D matrix array object from an array of angles

        Args:
            a : An array of angles in radians
        """

        if a.ndim != 1:
            raise ValueError('dimension mismatch')

        sa, ca = np.sin(a), np.cos(a)

        return cls(
            matrix = [
                [ca, -sa],
                [sa, ca.copy()],
            ],
            meta = meta,
        )

    @classmethod
    def from_3d_rotation(
        cls,
        v: Union[Vector3D, VectorArray3D],
        a: Union[Number, ndarray],
        meta: Union[MetaArrayDict, None] = None,
    ) -> MatrixArrayABC:
        """
        Generates new 3D matrix array object from a vector or vector array and
        an angle or one-dimensional ``numpy.ndarray`` of angles.
        Rotates by angle around vector.

        Args:
            v : A 3D vector or vector array
            a : An angle or array of angles in radians
        """

        if not isinstance(v, VectorArray3D) and not isinstance(a, ndarray):
            raise TypeError('neither v nor a are arrays')

        if isinstance(a, ndarray) and a.ndim != 1:
            raise ValueError('shape mismatch')

        if isinstance(v, VectorArray3D) and isinstance(a, ndarray):
            if len(v) != 1 and a.shape[0] != 1:
                if len(v) != a.shape[0]:
                    raise ValueError('length mismatch')

        ca = np.cos(a)
        oca = 1 - ca
        sa = np.sin(a)

        return cls(
            matrix = [
                [ca + (v.x ** 2) * oca, v.x * v.y * oca - v.z * sa, v.x * v.y * oca + v.y * sa],
                [v.y * v.x * oca + v.z * sa, ca + (v.y ** 2) * oca, v.y * v.z * oca - v.x * sa],
                [v.z * v.x * oca - v.y * sa, v.z * v.y * oca + v.x * sa, ca + (v.z ** 2) * oca],
            ],
            meta = meta,
        )
