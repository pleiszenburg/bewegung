# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/vector/single2ddist.py: Single 2D Vector with distance parameter

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

from typeguard import typechecked

from .single2d import Vector2D
from ..abc import Vector2DABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Vector2Ddist(Vector2D):
    """
    Immutable version of Vector2D with distance parameter
    """

    def __init__(self, x: float, y: float, dist: float):
        super().__init__(x = x, y = y,)
        self._dist = dist

    def __repr__(self) -> str:
        return f'<Vector2Ddist x={self._x:e} y={self._y:e} disty={self._dist:e}>'

    def mul(self, scalar: float):
        raise NotImplementedError()

    def as_vector(self) -> Vector2DABC:
        return Vector2D(self._x, self._y)

    def copy(self) -> Vector2DABC:
        return Vector2Ddist(self._x, self._y, self._dist)

    def update(self, x: float, y: float):
        raise NotImplementedError()

    def update_from_vector(self, other: Vector2DABC):
        raise NotImplementedError()

    @property
    def x(self) -> float:
        return self._x
    @x.setter
    def x(self, value: float):
        raise NotImplementedError()

    @property
    def y(self) -> float:
        return self._y
    @y.setter
    def y(self, value: float):
        raise NotImplementedError()

    @property
    def dist(self) -> float:
        return self._dist
    @dist.setter
    def dist(self, value: float):
        raise NotImplementedError()

    @classmethod
    def from_polar(cls, radius: float, angle: float) -> Vector2DABC:
        raise NotImplementedError()
