# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/vector/array2ddist.py: 2D Vector Array with distance parameter

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

from typing import List, Union

import numpy as np
from typeguard import typechecked

from .lib import dtype_np2py
from .single2ddist import Vector2Ddist
from .array2d import VectorArray2D
from ..abc import Dtype, Number, Vector2DABC, VectorArray2DABC, VectorIterable2D
from ..const import FLOAT_DEFAULT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class VectorArray2Ddist(VectorArray2D):
    """
    Immutable
    """

    def __init__(self, x: np.ndarray, y: np.ndarray, dist: np.ndarray):
        assert dist.ndim == 1
        assert x.shape[0] == y.shape[0] == dist.shape[0]
        assert x.dtype == y.dtype == dist.dtype
        x.setflags(write = False)
        y.setflags(write = False)
        dist.setflags(write = False)
        super().__init__(x = x, y = y,)
        self._dist = dist

    def __repr__(self) -> str:
        return f'<VectorArray2Ddist len={len(self):d}>'

    def __getitem__(self, idx: Union[int, slice]) -> Union[Vector2Ddist, VectorArray2DABC]:
        if isinstance(idx, int):
            dtype = dtype_np2py(self.dtype)
            return Vector2Ddist(dtype(self._x[idx]), dtype(self._y[idx]), dtype(self._dist[idx]), dtype = dtype)
        return VectorArray2Ddist(self._x[idx].copy(), self._y[idx].copy(), self._dist[idx].copy())

    def mul(self, scalar: Number):
        raise NotImplementedError()

    def as_vectorarray(self) -> VectorArray2DABC:
        return VectorArray2D(self._x.copy(), self._y.copy())

    def as_list(self) -> List[Vector2DABC]:
        dtype = dtype_np2py(self.dtype)
        return [
            Vector2Ddist(dtype(self._x[idx]), dtype(self._y[idx]), dtype(self._dist[idx]), dtype = dtype)
            for idx in range(len(self))
        ]

    def as_ndarray(self, dtype: Dtype = FLOAT_DEFAULT) -> np.ndarray:
        a = np.zeros((len(self), 3), dtype = self.dtype)
        a[:, 0], a[:, 1], a[:, 2] = self._x, self._y, self._dist
        return a if a.dtype == np.dtype(dtype) else a.astype(dtype)

    def as_type(self, dtype: Dtype) -> VectorArray2DABC:
        return self.copy() if self.dtype == np.dtype(dtype) else VectorArray2Ddist(
            self._x.astype(dtype), self._y.astype(dtype), self._dist.astype(dtype),
        )

    def copy(self) -> VectorArray2DABC:
        return VectorArray2Ddist(self._x.copy(), self._y.copy(), self._dist.copy())

    def update_from_vector(self, other: VectorArray2DABC):
        raise NotImplementedError()

    @property
    def dist(self) -> np.ndarray:
        return self._dist
    @dist.setter
    def dist(self, value: float):
        raise NotImplementedError()

    @classmethod
    def from_iterable(cls, obj: VectorIterable2D, dtype: Dtype = FLOAT_DEFAULT) -> VectorArray2DABC:
        if not isinstance(obj, list):
            obj = list(obj)
        assert all((isinstance(item, Vector2Ddist) for item in obj))
        x = np.zeros((len(obj),), dtype = dtype)
        y = np.zeros((len(obj),), dtype = dtype)
        dist = np.zeros((len(obj),), dtype = dtype)
        for idx, item in enumerate(obj):
            x[idx], y[idx], dist[idx] = item.x, item.y, item.dist
        return cls(x = x, y = y, dist = dist,)

    @classmethod
    def from_polar(cls, radius: np.ndarray, angle: np.ndarray) -> VectorArray2DABC:
        raise NotImplementedError()
