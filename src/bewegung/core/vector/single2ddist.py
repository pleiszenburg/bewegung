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

from typing import Type, Union

from .single2d import Vector2D
from ..abc import PyNumber, Vector2DABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Vector2Ddist(Vector2D):
    """
    Immutable version of :class:`bewegung.Vector2D` with distance parameter

    Args:
        x : x component. Must have the same type like ``y`` and ``dist``.
        y : y component. Must have the same type like ``x`` and ``dist``.
        dist : Distance component. Must have the same type like ``x`` and ``y``.
        dtype : Data type. Derived from ``x`` and ``y`` if not explicitly provided.
    """

    def __init__(self, x: PyNumber, y: PyNumber, dist: PyNumber, dtype: Union[Type, None] = None):

        super().__init__(x = x, y = y, dtype = dtype)
        assert isinstance(dist, self._dtype)
        self._dist = dist

    def __repr__(self) -> str:
        """
        String representation for interactive use
        """

        if self._dtype == int:
            return f'<Vector2Ddist x={self._x:d} y={self._y:d} dist={self._dist:d} dtype={self._dtype.__name__:s}>'
        return f'<Vector2Ddist x={self._x:e} y={self._y:e} dist={self._dist:e} dtype={self._dtype.__name__:s}>'

    def mul(self, scalar: PyNumber):
        ""
        raise NotImplementedError()

    def as_vector(self) -> Vector2DABC:
        """
        Exports a vector without distance component
        """

        return Vector2D(self._x, self._y, dtype = self._dtype)

    def copy(self) -> Vector2DABC:
        """
        Copies vector with distance component
        """

        return type(self)(self._x, self._y, self._dist, dtype = self._dtype)

    def update(self, x: PyNumber, y: PyNumber):
        ""
        raise NotImplementedError()

    def update_from_vector(self, other: Vector2DABC):
        ""
        raise NotImplementedError()

    @property
    def x(self) -> PyNumber:
        """
        x component
        """

        return self._x

    @x.setter
    def x(self, value: PyNumber):
        ""
        raise NotImplementedError()

    @property
    def y(self) -> PyNumber:
        """
        y component
        """

        return self._y

    @y.setter
    def y(self, value: PyNumber):
        ""
        raise NotImplementedError()

    @property
    def dist(self) -> PyNumber:
        """
        Distance component
        """

        return self._dist

    @dist.setter
    def dist(self, value: PyNumber):
        ""
        raise NotImplementedError()

    @classmethod
    def from_polar(cls, radius: PyNumber, angle: PyNumber) -> Vector2DABC:
        ""
        raise NotImplementedError()
