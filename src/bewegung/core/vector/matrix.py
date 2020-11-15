# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/vector/matrix.py: Simple 2x2/3x3 matrix for rotations

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

from math import cos, sin
from typing import List, Tuple, Type, Union

try:
    import numpy as np
    from numpy import ndarray
except ModuleNotFoundError:
    np, ndarray = None, None
from typeguard import typechecked

from ..abc import Dtype, MatrixABC, PyNumber, Vector2DABC, Vector3DABC
from ..const import FLOAT_DEFAULT
from .single2d import Vector2D
from .single3d import Vector3D

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Matrix(MatrixABC):
    """
    Mutable
    """

    def __init__(self, matrix = List[List[PyNumber]], dtype: Union[Type, None] = None):

        lines = len(matrix)
        assert lines in (2, 3) # allow 2D and 3D
        assert all((len(line) == lines for line in matrix))

        if dtype is None:
            dtype = type(matrix[0][0])
        else:
            assert isinstance(matrix[0][0], dtype)
        assert all((all((isinstance(number, dtype) for number in line)) for line in matrix))

        self._dtype = dtype
        self._matrix = matrix

    def __repr__(self) -> str:
        return f'<Matrix shape={len(self._matrix):d}x{len(self._matrix):d} dtype={self._dtype.__name__:s}>'

    def __matmul__(self, vector: Union[Vector2DABC, Vector3DABC]) -> Union[Vector2DABC, Vector3DABC]:

        vector = vector.as_tuple()
        assert len(self._matrix) == len(vector)

        values = [
            sum([item_a * item_b for item_a, item_b in zip(line, vector)])
            for line in self._matrix
        ]

        return Vector2D(*values) if len(vector) == 2 else Vector3D(*values)

    def __getitem__(self, index: Tuple[int, int]) -> PyNumber:
        return self._matrix[index[0]][index[1]]

    def __setitem__(self, index: Tuple[int, int], value: PyNumber):
        self._matrix[index[0]][index[1]] = self._dtype(value)

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> ndarray:
        if np is None:
            raise NotImplementedError('numpy is not available')
        return np.array(self._matrix, dtype = dtype)

    @property
    def dtype(self) -> Type:
        return self._dtype

    @classmethod
    def from_ndarray(cls, matrix: np.ndarray, dtype: Type = float) -> MatrixABC:

        assert matrix.ndim == 2
        assert matrix.shape in ((2, 2), (3, 3))

        matrix = matrix.tolist()
        if isinstance(matrix[0][0], int):
            matrix = [[dtype(item) for item in line] for line in matrix]

        return cls(matrix, dtype = dtype)

    @classmethod
    def from_2d_rotation(cls, a: PyNumber) -> MatrixABC:

        return cls([
            [cos(a), -sin(a)],
            [sin(a), cos(a)],
        ])

    @classmethod
    def from_3d_rotation(cls, v: Vector3DABC, a: PyNumber) -> MatrixABC:

        ca = cos(a)
        oca = 1 - ca
        sa = sin(a)

        return cls([
            [ca + (v.x ** 2) * oca, v.x * v.y * oca - v.z * sa, v.x * v.y * oca + v.y * sa],
            [v.y * v.x * oca + v.z * sa, ca + (v.y ** 2) * oca, v.y * v.z * oca - v.x * sa],
            [v.z * v.x * oca - v.y * sa, v.z * v.y * oca + v.x * sa, ca + (v.z ** 2) * oca],
        ])
