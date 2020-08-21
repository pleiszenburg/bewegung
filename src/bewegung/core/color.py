# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/color.py: Simple RGBA Color handling

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

from typing import Tuple

from typeguard import typechecked

from .abc import ColorABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Color(ColorABC):
    """
    Immutable.
    """

    def __init__(self,
        r: int,
        g: int,
        b: int,
        a: int = 255,
    ):

        assert 0 <= r <= 255
        assert 0 <= g <= 255
        assert 0 <= b <= 255
        assert 0 <= a <= 255

        self._r, self._g, self._b, self._a = r, g, b, a

    def __repr__(self) -> str:

        return f'<Color r={self._r:d} g={self._g:d} b={self._b:d} a={self._a:d}>'

    @property
    def r(self) -> int:
        return self._r

    @property
    def g(self) -> int:
        return self._g

    @property
    def b(self) -> int:
        return self._b

    @property
    def a(self) -> int:
        return self._a

    def as_hex(self, alpha: bool = True) -> str:

        if not alpha:
            return f'{self._r:02x}{self._g:02x}{self._b:02x}'

        return f'{self._r:02x}{self._g:02x}{self._b:02x}{self._a:02x}'

    def as_rgba_float(self) -> Tuple[float, float, float, float]:

        return self._r / 255, self._g / 255, self._b / 255, self._a / 255

    def as_rgba_int(self) -> Tuple[int, int, int, int]:

        return self._r, self._g, self._b, self._a

    @classmethod
    def from_rgba_float(cls,
        r: float,
        g: float,
        b: float,
        a: float = 1.0,
    ) -> ColorABC:

        assert 0.0 <= r <= 1.0
        assert 0.0 <= g <= 1.0
        assert 0.0 <= b <= 1.0
        assert 0.0 <= a <= 1.0

        return cls(
            r = round(r * 255),
            g = round(g * 255),
            b = round(b * 255),
            a = round(a * 255),
        )

    @classmethod
    def from_hex(cls, raw: str) -> ColorABC:

        if raw.startswith('#'):
            raw = raw[1:]

        assert len(raw) in (6, 8)

        return cls(**{
            color: int(component, base = 16)
            for color, component in zip(
                ('r', 'g', 'b', 'a'),
                (raw[idx:idx+2] for idx in range(0, 8, 2)),
            )
            if not (color == 'a' and len(component) == 0)
        })
