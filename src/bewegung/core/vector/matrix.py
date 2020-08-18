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
from typing import List, Union

import numpy as np
from typeguard import typechecked

from ..abc import Dtype, MatrixABC, Vector2DABC, Vector3DABC
from ..const import FLOAT_DEFAULT
from .single2d import Vector2D
from .single3d import Vector3D

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Matrix(MatrixABC):

    def __init__(self, matrix = List[List[float]]):

        lines = len(matrix)
        assert lines in (2, 3) # allow 2D and 3D
        assert all((len(line) == lines for line in matrix))

        self._matrix = matrix

    def __matmul__(self, vector: Union[Vector2DABC, Vector3DABC]) -> Union[Vector2DABC, Vector3DABC]:

        vector = vector.as_tuple()
        assert len(self._matrix) == len(vector)

        values = [
            sum([item_a * item_b for item_a, item_b in zip(line, vector)])
            for line in self._matrix
        ]

        return Vector2D(*values) if len(vector) == 2 else Vector3D(*values)

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> np.ndarray:

        return np.array(self._matrix, dtype = dtype)

    @classmethod
    def from_ndarray(cls, matrix: np.ndarray) -> MatrixABC:

        assert matrix.ndim == 2
        assert matrix.shape in ((2, 2), (3, 3))

        matrix = matrix.tolist()
        if isinstance(matrix[0][0], int):
            matrix = [[float(item) for item in line] for line in matrix]

        return cls(matrix)

    @classmethod
    def from_2d_rotation(cls, a: float) -> MatrixABC:

        return cls([
            [cos(a), -sin(a)],
            [sin(a), cos(a)],
        ])

    @classmethod
    def from_3d_rotation(cls, v: Vector3DABC, a: float) -> MatrixABC:

        ca = cos(a)
        oca = 1 - ca
        sa = sin(a)

        return cls([
            [ca + (v.x ** 2) * oca, v.x * v.y * oca - v.z * sa, v.x * v.y * oca + v.y * sa],
            [v.y * v.x * oca + v.z * sa, ca + (v.y ** 2) * oca, v.y * v.z * oca - v.x * sa],
            [v.z * v.x * oca - v.y * sa, v.z * v.y * oca + v.x * sa, ca + (v.z ** 2) * oca],
        ])
