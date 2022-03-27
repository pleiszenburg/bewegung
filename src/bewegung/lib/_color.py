# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/lib/_color.py: Simple RGBA Color handling

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

from math import floor
from typing import Tuple

from ._abc import ColorABC
from ._typeguard import typechecked

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Color(ColorABC):
    """
    Common infrastructure for working with RGBA colors in different formats.

    Color objects are immutable.

    Args:
        r : red channel 0...255 (uint8)
        g : green channel 0...255 (uint8)
        b : blue channel 0...255 (uint8)
        a : alpha channel 0...255 (uint8), opaque by default
    """

    def __init__(self,
        r: int,
        g: int,
        b: int,
        a: int = 255,
    ):

        if not (0 <= r <= 255):
            raise ValueError('red color channel out of bounds (0...255)')
        if not (0 <= g <= 255):
            raise ValueError('green color channel out of bounds (0...255)')
        if not (0 <= b <= 255):
            raise ValueError('blue color channel out of bounds (0...255)')
        if not (0 <= a <= 255):
            raise ValueError('alpha color channel out of bounds (0...255)')

        self._r, self._g, self._b, self._a = r, g, b, a

    def __repr__(self) -> str:

        return f'<Color r={self._r:d} g={self._g:d} b={self._b:d} a={self._a:d}>'

    @property
    def r(self) -> int:
        """
        red channel
        """

        return self._r

    @property
    def g(self) -> int:
        """
        green channel
        """

        return self._g

    @property
    def b(self) -> int:
        """
        blue channel
        """

        return self._b

    @property
    def a(self) -> int:
        """
        alpha channel
        """

        return self._a

    def as_hex(self, alpha: bool = True) -> str:
        """
        Exports color as hexadecimal string

        Args:
            alpha : Allows to disable alpha channel on export
        """

        if not alpha:
            return f'{self._r:02x}{self._g:02x}{self._b:02x}'

        return f'{self._r:02x}{self._g:02x}{self._b:02x}{self._a:02x}'

    def as_rgba_float(self) -> Tuple[float, float, float, float]:
        """
        Exports color a tuple of floats 0.0...1.0
        """

        return self._r / 255, self._g / 255, self._b / 255, self._a / 255

    def as_rgba_int(self) -> Tuple[int, int, int, int]:
        """
        Exports color a tuple of ints 0...255 (uint8)
        """

        return self._r, self._g, self._b, self._a

    def as_opaque(self) -> ColorABC:
        """
        Exports color as a new, fully opaque version of itself
        """

        return type(self)(self._r, self._g, self._b, 255)

    def as_transparent(self) -> ColorABC:
        """
        Exports color as a new, fully transparent version of itself
        """

        return type(self)(self._r, self._g, self._b, 0)

    @classmethod
    def from_rgba_float(cls,
        r: float,
        g: float,
        b: float,
        a: float = 1.0,
    ) -> ColorABC:
        """
        Imports color from floats

        Args:
            r : red channel 0.0...1.0
            g : green channel 0.0...1.0
            b : blue channel 0.0...1.0
            a : alpha channel 0.0...1.0, opaque by default
        """

        if not (0.0 <= r <= 1.0):
            raise ValueError('red color channel out of bounds (0.0...1.0)')
        if not (0.0 <= g <= 1.0):
            raise ValueError('green color channel out of bounds (0.0...1.0)')
        if not (0.0 <= b <= 1.0):
            raise ValueError('blue color channel out of bounds (0.0...1.0)')
        if not (0.0 <= a <= 1.0):
            raise ValueError('alpha color channel out of bounds (0.0...1.0)')

        return cls(
            r = round(r * 255),
            g = round(g * 255),
            b = round(b * 255),
            a = round(a * 255),
        )

    @classmethod
    def from_hex(cls, raw: str) -> ColorABC:
        """
        Imports color from a hexadecimal string

        Args:
            raw : Accepts strings both with and without alpha channel. Opaque by default.
        """

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

    @classmethod
    def from_hsv(cls,
        h: float,
        s: float,
        v: float,
    ):
        """
        Imports color from HSV

        Args:
            h : hue 0.0...360.0
            s : saturation 0.0...1.0
            v : value (brightness) 0.0...1.0
        """

        if not (0.0 <= h <= 360.0):
            raise ValueError('hue value out of bounds (0.0...360.0)')
        if not (0.0 <= s <= 1.0):
            raise ValueError('saturation value out of bounds (0.0...1.0)')
        if not (0.0 <= v <= 1.0):
            raise ValueError('"value" (brightness) value out of bounds (0.0...1.0)')

        hi = floor(h / 60)

        f = h / 60 - hi

        p = round(255 * v * (1 - s))
        q = round(255 * v * (1 - s * f))
        t = round(255 * v * (1 - s * (1 - f)))
        v = round(255 * v)

        if hi == 1:
            return cls(q, v, p)
        if hi == 2:
            return cls(p, v, t)
        if hi == 3:
            return cls(p, q, v)
        if hi == 4:
            return cls(t, p, v)
        if hi == 5:
            return cls(v, p, q)
        if hi in (0, 6):
            return cls(v, t, p)

        raise ValueError('Conversion from HSV to RGB failed')
