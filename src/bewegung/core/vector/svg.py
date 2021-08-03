# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/vector/svg.py: SVG output for vectors

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

from typing import Union

from typeguard import typechecked

from ..abc import VectorABC, VectorArrayABC, NumberTypes

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@typechecked
class Svg:
    """
    Wrap vectors into SVG
    """

    def __init__(self, vec: Union[VectorABC, VectorArrayABC], size: NumberTypes = 300):

        size = float(size)
        assert size > 0
        self._size = size

        self._radius = 0
        self._vectors = []

        if isinstance(vec, VectorABC):
            self._add_vector(vec)
        else:
            self._add_vectors(vec)

    def _add_vector(self, vector: VectorABC):

        if abs(vector.x) > self._radius:
            self._radius = abs(vector.x)
        if abs(vector.y) > self._radius:
            self._radius = abs(vector.y)

        self._vectors.append(vector)

    def _add_vectors(self, vectors: VectorArrayABC):

        for vector in vectors:
            self._add_vector(vector)

    def _render_grid(self, scale_factor: float):

        return (
            '<polyline '
            'fill="none" '
            'stroke="#808080" '
            f'stroke-width="{2*scale_factor:e}" '
            f'points="{-self._radius:e},0.0 {self._radius:e},0.0" '
            'opacity="1.0" />'
            '<polyline '
            'fill="none" '
            'stroke="#000000" '
            f'stroke-width="{2*scale_factor:e}" '
            f'points="0.0,{-self._radius:e} 0.0,{self._radius:e}" '
            'opacity="1.0" />'
        )

    def _render_vector(self, vector: VectorABC, scale_factor: float, inverse_radius: float) -> str:

        return (
            '<polyline '
            'fill="none" '
            'stroke="#FF0000" '
            f'stroke-width="{2*scale_factor:e}" '
            f'points="0.0,0.0 {vector.x:e},{vector.y:e}" '
            'opacity="1.0" />'
        )

    def render(self) -> str:

        assert len(self._vectors) > 0
        assert self._radius > 0

        scale_factor = 2 * self._radius / self._size
        inverse_radius = 1 / self._radius

        return (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{self._size:e}" height="{self._size:e}" '
            f'viewBox="{-self._radius:e} {-self._radius:e} {2*self._radius:e} {2*self._radius:e}" '
            f'preserveAspectRatio="xMinYMin meet">'
            f'<g transform="matrix(1,0,0,-1,0,0)">'
            f'{self._render_grid(scale_factor):s}'
            f'{"".join([self._render_vector(vec, scale_factor, inverse_radius) for vec in self._vectors]):s}'
            '</g>'
            '</svg>'
        )
