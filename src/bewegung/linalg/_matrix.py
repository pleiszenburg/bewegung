# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/_matrix.py: Simple 2x2/3x3 matrix for rotations

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

from math import cos, sin, isclose
from numbers import Number
from typing import Any, Tuple, Union

from ..lib import typechecked
from ._abc import (
    Dtype,
    Iterable,
    MatrixABC,
    MetaDict,
    NotImplementedType,
    Numbers,
    NumberType,
)
from ._array import VectorArray
from ._array2d import VectorArray2D
from ._array3d import VectorArray3D
from ._const import FLOAT_DEFAULT
from ._lib import dtype_name
from ._numpy import np, ndarray
from ._single import Vector
from ._single2d import Vector2D
from ._single3d import Vector3D

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Matrix(MatrixABC):
    """
    A simple matrix implementation for transforming vectors and vector arrays

    Mutable.

    Args:
        matrix : 2D or 3D arrangement in a list of lists containing Python numbers
        dtype : Data type. Derived from entries in ``matrix`` if not explicitly provided.
        meta : A dict holding arbitrary metadata
    """

    def __init__(self, matrix = Iterable[Iterable[Numbers]], dtype: Union[NumberType, None] = None, meta: Union[MetaDict, None] = None):

        matrix = [list(row) for row in matrix] # convert to lists or copy lists

        rows = len(matrix)
        if rows not in (2, 3): # allow 2D and 3D
            raise ValueError('neither 2D nor 3D')
        if not all((len(row) == rows for row in matrix)): # check columns
            raise ValueError('number of rows and columns do not match')

        if dtype is None:
            dtype = type(matrix[0][0])
            if not all(all(isinstance(col, dtype) for col in row) for row in matrix):
                raise TypeError('can not guess dtype - inconsistent')
        else:
            matrix = [[dtype(col) for col in row] for row in matrix]

        self._matrix = matrix
        self._meta = {} if meta is None else dict(meta)

    def __repr__(self) -> str:
        """
        String representation for interactive use
        """

        values = ',\n'.join([
            f' ({", ".join([str(col) for col in row]):s})' for row in self._matrix
        ])

        return f'<Matrix values=(\n{values:s}\n) ndim={len(self._matrix):d} dtype={dtype_name(self.dtype):s}>'

    def __matmul__(self, other: Any) -> Union[Vector, VectorArray, NotImplementedType]:
        """
        Multiplies the matrix with a vector or array of vectors
        and returns the resulting new vector or array of vectors.
        Raises an exception if matrix and vector or
        array of vectors have different numbers of dimensions.

        Args:
            other : A 2D or 3D vector or array of vectors
        """

        if not any(isinstance(other, t) for t in (Vector, VectorArray)):
            return NotImplemented

        if self.ndim != other.ndim:
            raise ValueError('dimension mismatch')

        vector_tuple = other.as_tuple(copy = False) if isinstance(other, VectorArray) else other.as_tuple()

        if isinstance(other, VectorArray) and np is not None:
            sum_ = lambda x: np.sum(np.array(x), axis = 0)
        else:
            sum_ = sum

        values = [
            sum_([
                matrix_element * vector_coordinate
                for matrix_element, vector_coordinate in zip(matrix_row, vector_tuple)
            ])
            for matrix_row in self._matrix
        ]

        if isinstance(other, Vector):
            return Vector2D(*values) if len(vector_tuple) == 2 else Vector3D(*values)

        return VectorArray2D(*values) if len(vector_tuple) == 2 else VectorArray3D(*values)

    def __getitem__(self, index: Tuple[int, int]) -> Number:
        """
        Item access, returns value at position

        Args:
            index : Row and column index
        """

        return self._matrix[index[0]][index[1]]

    def __setitem__(self, index: Tuple[int, int], value: Number):
        """
        Item access, sets new value at position

        Args:
            index : Row and column index
            value : New value
        """

        self._matrix[index[0]][index[1]] = self.dtype(value)

    def __eq__(self, other: Any) -> Union[bool, NotImplementedType]:
        """
        Equality check between matrices

        Args:
            other : Another matrix
        """

        if not isinstance(other, MatrixABC):
            return NotImplemented

        if self.ndim != other.ndim:
            return False

        return self.as_tuple() == other.as_tuple()

    def __mod__(self, other: Any) -> Union[bool, NotImplementedType]:
        """
        Is-close check between matrices

        Args:
            other : Another matrix
        """

        if not isinstance(other, MatrixABC):
            return NotImplemented

        if self.ndim != other.ndim:
            return False

        return all(
            isclose(number_a, number_b)
            for line_a, line_b in zip(self.as_tuple(), other.as_tuple())
            for number_a, number_b in zip(line_a, line_b)
        )

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> ndarray:
        """
        Exports matrix as a ``numpy.ndarry`` object, shape ``(2, 2)`` or ``(3, 3)``.

        Args:
            dtype : Desired ``numpy`` data type of new vector
        """

        if np is None:
            raise NotImplementedError('numpy is not available')

        return np.array(self._matrix, dtype = dtype)

    def as_tuple(self) -> Tuple[Tuple[Numbers, ...], ...]:
        """
        Exports matrix as a tuple of tuples
        """

        return tuple(tuple(item) for item in self._matrix)

    def copy(self) -> MatrixABC:
        """
        Copies matrix & meta data
        """

        return type(self)(matrix = [row.copy() for row in self._matrix], dtype = self.dtype, meta = self._meta.copy())

    @property
    def dtype(self) -> NumberType:
        """
        (Python) data type of matrix components
        """

        return type(self._matrix[0][0])

    @property
    def ndim(self) -> int:
        """
        Number of dimensions, either ``2`` or ``3``.
        """

        return len(self._matrix)

    @property
    def meta(self) -> MetaDict:
        """
        meta data dict
        """

        return self._meta

    @classmethod
    def from_ndarray(cls, matrix: ndarray, dtype: NumberType = float, meta: Union[MetaDict, None] = None) -> MatrixABC:
        """
        Generates new matrix object from ``numpy.ndarray`` object
        of shape ``(2, 2)`` or ``(3, 3)``

        Args:
            matrix : Input data
            dtype : Desired (Python) data type of matrix
            meta : A dict holding arbitrary metadata
        """

        if matrix.ndim != 2:
            raise ValueError('shape mismatch - ndim != 2')
        if matrix.shape not in ((2, 2), (3, 3)):
            raise ValueError('shape mismatch - not NxN')

        matrix = [[dtype(col) for col in row] for row in matrix.tolist()]

        return cls(matrix, dtype = dtype, meta = meta,)

    @classmethod
    def from_2d_rotation(cls, a: Number, meta: Union[MetaDict, None] = None) -> MatrixABC:
        """
        Generates new 2D matrix object from an angle

        Args:
            a : An angle in radians
            meta : A dict holding arbitrary metadata
        """

        sa, ca = sin(a), cos(a)

        return cls(
            [
                [ca, -sa],
                [sa, ca],
            ],
            meta = meta,
        )

    @classmethod
    def from_3d_rotation(cls, v: Vector3D, a: Number, meta: Union[MetaDict, None] = None) -> MatrixABC:
        """
        Generates new 3D matrix object from a vector and an angle.
        Rotates by angle around vector.

        Args:
            v : A 3D vector
            a : An angle in radians
            meta : A dict holding arbitrary metadata
        """

        ca = cos(a)
        oca = 1 - ca
        sa = sin(a)

        return cls(
            [
                [ca + (v.x ** 2) * oca, v.x * v.y * oca - v.z * sa, v.x * v.y * oca + v.y * sa],
                [v.y * v.x * oca + v.z * sa, ca + (v.y ** 2) * oca, v.y * v.z * oca - v.x * sa],
                [v.z * v.x * oca - v.y * sa, v.z * v.y * oca + v.x * sa, ca + (v.z ** 2) * oca],
            ],
            meta = meta,
        )
