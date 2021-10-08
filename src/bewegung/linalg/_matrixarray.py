# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/_matrixarray.py: Array of simple 2x2/3x3 matrices for rotations

    Copyright (C) 2020-2021 Sebastian M. Ernst <ernst@pleiszenburg.de>

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
from typing import Any, List, Tuple, Type, Union

from ..lib import typechecked
from ._abc import (
    Dtype,
    MatrixArrayABC,
    NotImplementedType,
    Vector2DABC,
    Vector3DABC,
    VectorArray2DABC,
    VectorArray3DABC,
)
from ._const import FLOAT_DEFAULT
from ._array import VectorArray
from ._lib import dtype_np2py
from ._numpy import np, ndarray
from ._single import Vector
from ._single2d import Vector2D
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

    def __init__(self, matrix = List[List[ndarray]]):

        rows = len(matrix)
        assert rows in (2, 3) # allow 2D and 3D
        assert all((len(row) == rows for row in matrix))

        self._length = matrix[0][0].shape[0]
        self._dtype = matrix[0][0].dtype

        assert all(
            all((
                item.ndim == 1,
                item.shape[0] == self._length,
                item.dtype == self._dtype,
            ))
            for line in matrix for item in line
        )

        self._matrix = matrix
        self._iterstate = 0

    def __repr__(self) -> str:
        """
        String representation for interactive use
        """

        dtype = getattr(
            self._dtype, '__name__',
            str(self._dtype), # fallback, numpy
        )

        return f'<MatrixArray ndim={len(self._matrix):d} dtype={dtype:s} len={len(self):d}>'

    def __len__(self) -> int:
        """
        Length of array
        """

        return self._length

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
            ]))
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
            return MatrixArray([
                [col[idx].copy() for col in row]
                for row in self._matrix
            ])

        dtype = dtype_np2py(self.dtype)

        return MatrixArray([
            [dtype(col[idx]) for col in row]
            for row in self._matrix
        ])

    def __iter__(self) -> MatrixArrayABC:
        """
        Iterator interface (1/2)
        """

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

        return [self[idx] for idx in range(len(self))]

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
        Copies matrix array
        """

        return type(self)([
            [col.copy() for col in row]
            for row in self._matrix
        ])

    @property
    def dtype(self) -> Type:
        """
        (Python) data type of matrix components
        """

        return self._dtype

    @property
    def ndim(self) -> int:
        """
        Number of dimensions, either ``2`` or ``3``.
        """

        return len(self._matrix)

    @classmethod
    def from_ndarray(cls, matrix_array: ndarray) -> MatrixArrayABC:
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

        return cls([
            [matrix_array[:, row, col] for col in range(ndim)]
            for row in range(ndim)
        ])

    @classmethod
    def from_2d_rotation(cls, a: ndarray) -> MatrixArrayABC:
        """
        Generates new 2D matrix array object from an array of angles

        Args:
            a : An array of angles in radians
        """

        if a.ndim != 1:
            raise ValueError('dimension mismatch')

        sa, ca = np.sin(a), np.cos(a)

        return cls([
            [ca, -sa],
            [sa, ca.copy()],
        ])

    @classmethod
    def from_3d_rotation(cls, v: Union[Vector3D, VectorArray3D], a: Union[Number, ndarray]) -> MatrixArrayABC:
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

        return cls([
            [ca + (v.x ** 2) * oca, v.x * v.y * oca - v.z * sa, v.x * v.y * oca + v.y * sa],
            [v.y * v.x * oca + v.z * sa, ca + (v.y ** 2) * oca, v.y * v.z * oca - v.x * sa],
            [v.z * v.x * oca - v.y * sa, v.z * v.y * oca + v.x * sa, ca + (v.z ** 2) * oca],
        ])
