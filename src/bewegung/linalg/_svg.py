# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/_svg.py: SVG output for vectors

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

from math import ceil, floor, log10, pi
from numbers import Number
from typing import Union

from ..lib import Color, typechecked
from ._array import VectorArray
from ._single import Vector

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Svg:
    """
    Wrap vectors into SVG
    """

    def __init__(self, vec: Union[Vector, VectorArray], size: Number = 300):

        size = float(size)
        assert size > 0
        self._size = size

        self._vectors = []
        self._radius = 0
        self._view = 0
        self._scale_factor = 0
        self._step = 0

        if isinstance(vec, Vector):
            self._add_vector(vec)
        else:
            self._add_vectors(vec)

    def _add_vector(self, vector: Vector):

        self._update(vector.x)
        self._update(vector.y)

        self._vectors.append(vector)

    def _add_vectors(self, vectors: VectorArray):

        for vector in vectors:
            self._add_vector(vector)

    def _update(self, value: Number):

        value = abs(float(value))

        if value <= self._radius:
            return

        self._radius = value

        self._scale_factor = 2 * self._radius / self._size

        pos = floor(log10(self._radius))
        self._view = ceil(self._radius / (10 ** pos)) * (10 ** pos)

        self._step = 10 ** floor(log10(self._radius))

    def _line(
        self,
        x1: float = 0.0, y1: float = 0.0,
        x2: float = 0.0, y2: float = 0.0,
        color: str = '#FF0000',
        opacity: float = 1.0,
        width: float = 1.0,
        dashed: bool = False,
        m1: bool = False,
        m2: bool = False,
    ):

        assert width > 0
        assert len(color) == 7 and color[0] == '#'
        assert 0.0 <= opacity <= 1.0

        if (x1, y1) == (x2, y2):
            return ''

        dashes = f'stroke-dasharray="{self._scale_factor*4:e} {self._scale_factor*1:e}" ' if dashed else ''
        markerid = f'arrow_{hash((x1, y1, x2, y2)):x}' if m1 or m2 else ''
        markerfactor = self._size / 50
        marker = (
            '<defs>'
            f'<marker id="{markerid:s}" '
            'orient="auto" '
            f'markerWidth="{markerfactor*2:e}" markerHeight="{markerfactor*1.5:e}" '
            f'refX="{markerfactor*2:e}" refY="{markerfactor*0.75:e}">'
            f'<path d="M0,0 V{markerfactor*1.5:e} L{markerfactor*2:e},{markerfactor*0.75:e} Z" '
            f'fill="{color:s}"/>'
            '</marker>'
            '</defs>'
        ) if m1 or m2 else ''
        markerstart = f'marker-start="url(#{markerid:s})" ' if m1 else ''
        markerend = f'marker-end="url(#{markerid:s})" ' if m2 else ''

        return (
            f'{marker:s}'
            '<polyline '
            'fill="none" '
            f'stroke="{color:s}" '
            f'stroke-width="{self._scale_factor * width:e}" '
            f'points="{x1:e},{y1:e} {x2:e},{y2:e}" '
            f'opacity="{opacity:e}" '
            f'{dashes:s}'
            f'{markerstart:s}'
            f'{markerend:s}'
            '/>'
        )

    def _grid(self):

        lines = [
            self._line(x1 = -self._view, x2 = self._view, color = '#808080'),
            self._line(y1 = -self._view, y2 = self._view, color = '#808080'),
        ]

        for idx in range(-10, 11):
            if idx == 0:
                continue
            tock = idx % 10 == 0
            val = float(idx * self._step)
            lines.append(self._line(
                x1 = -self._view, y1 = val,
                x2 = self._view, y2 = val,
                color = '#808080' if tock else '#C0C0C0',
                dashed = True,
            ))
            lines.append(self._line(
                x1 = val, y1 = -self._view,
                x2 = val, y2 = self._view,
                color = '#808080' if tock else '#C0C0C0',
                dashed = True,
            ))

        return ''.join(lines)

    def _vector(self, vector: Vector) -> str:

        color = Color.from_hsv(vector.angle * 180 / pi, 1.0, 1.0).as_hex(alpha = False)

        return self._line(x2 = vector.x, y2 = vector.y, color = f'#{color:s}', m2 = True)

    def render(self) -> str:

        assert len(self._vectors) > 0
        assert self._radius > 0
        assert self._view >= self._radius
        assert self._scale_factor > 0

        return (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{self._size:e}" height="{self._size:e}" '
            f'viewBox="{-self._view:e} {-self._view:e} {2*self._view:e} {2*self._view:e}" '
            f'preserveAspectRatio="xMinYMin meet">'

            f'<g transform="matrix(1,0,0,-1,0,0)">' # invert y axis
            f'{self._grid():s}'
            f'{"".join([self._vector(vec) for vec in self._vectors]):s}'
            '</g>'

            '<style>'
            f'.step {{ font-family: monospace; font-size: {15*self._scale_factor:e}px; fill: #C0C0C0; }}'
            '</style>'
            f'<text x="{-self._view+5*self._scale_factor:e}" y="{self._view-5*self._scale_factor:e}" class="step">'
            f'tick={self._step:0.0e}'
            '</text>'

            '</svg>'
        )
