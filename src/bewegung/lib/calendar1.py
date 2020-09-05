# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/lib/calendar1.py: Circular calendar

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

import calendar
from datetime import datetime
import math
from typing import List, Union

from PIL.Image import Image, new
from typeguard import typechecked

from ..core.color import Color
from ..core.drawingboard import DrawingBoard, Pango
from ..core.vector import Matrix, Vector2D

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class _Background(DrawingBoard):

    _twopi = 2 * math.pi
    _halfpi = math.pi / 2

    def draw_ticks(self,
        r1: float,
        r2: float,
        ticks: range,
        line_color: Color,
        line_width: float,
        zero: float = 0.0,
        length: Union[float, None] = None
    ):

        if length is None:
            length = len(ticks)

        af = self._twopi / length

        for tick in ticks:
            angle = (tick - zero) * af - self._halfpi
            self.draw_polygon(
                Vector2D.from_polar(r1, angle),
                Vector2D.from_polar(r2, angle),
                line_color = line_color,
                line_width = line_width,
            )

    def draw_labels(self,
        r: float,
        labels: List[str],
        font: Pango.FontDescription,
        font_color: Color,
        zero: float = 0.0,
        length: Union[float, None] = None
    ):

        if length is None:
            length = len(labels)

        af = self._twopi / length

        for idx, label in enumerate(labels):
            angle = (idx - zero) * af - self._halfpi
            self.draw_text(
                text = label,
                point = Vector2D.from_polar(r, angle),
                font = font,
                font_color = Color(255, 0, 0),
            )

@typechecked
class _Foreground(DrawingBoard):

    _twopi = 2 * math.pi
    _days_in_decade = {}

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._days_in_decade.update({
            decade: sum([
                self._days_in_year(decade + year)
                for year in range(10)
            ])
            for decade in range(1970, 2070 + 10, 10)
        })

    def draw_hands(self, dt: datetime, factor: float, color: Color):

        self.draw_circle(
            Vector2D(0.0, 0.0),
            16 * factor,
            line_color = color,
            line_width = 2.0 * factor,
        )

        mr = Matrix.from_2d_rotation(self._angle_from_day_in_century(dt))
        self.draw_polygon(
            mr @ (Vector2D(-9.0, -13.0) * factor),
            mr @ (Vector2D(-13.0, -75.0) * factor),
            mr @ (Vector2D(0, -103.0) * factor),
            mr @ (Vector2D(13.0, -75.0) * factor),
            mr @ (Vector2D(9.0, -13.0) * factor),
            line_color = color,
            line_width = 2.0 * factor,
        ) # decade in century

        mr = Matrix.from_2d_rotation(self._angle_from_day_in_decade(dt))
        self.draw_polygon(
            mr @ (Vector2D(-5.0, -15.0) * factor),
            mr @ (Vector2D(-7.0, -145.0) * factor),
            mr @ (Vector2D(0, -165.0) * factor),
            mr @ (Vector2D(7.0, -145.0) * factor),
            mr @ (Vector2D(5.0, -15.0) * factor),
            line_color = color,
            line_width = 2.0 * factor,
        ) # year in decade

        mr = Matrix.from_2d_rotation(self._angle_from_day_in_year(dt))
        self.draw_polygon(
            mr @ (Vector2D(0, -16.0) * factor),
            mr @ (Vector2D(0.0, -220.0) * factor),
            line_color = color,
            line_width = 2.0 * factor,
        ) # day in year

    @staticmethod
    def _days_in_year(year: int) -> int:
        return 366 if calendar.isleap(year) else 365

    @staticmethod
    def _decade_from_year(year: int):
        return int(year / 10) * 10

    @staticmethod
    def _day_in_year(dt: datetime):
        return dt.timetuple().tm_yday

    @classmethod
    def _day_in_decade(cls, dt: datetime):
        return sum([
            cls._days_in_year(previous_year)
            for previous_year in range(cls._decade_from_year(dt.year), dt.year)
        ]) + cls._day_in_year(dt)

    @classmethod
    def _angle_from_day_in_year(cls, dt: datetime) -> float:
        return cls._twopi * cls._day_in_year(dt) / cls._days_in_year(dt.year)

    @classmethod
    def _angle_from_day_in_decade(cls, dt: datetime) -> float:
        return cls._twopi * cls._day_in_decade(dt) / cls._days_in_decade[cls._decade_from_year(dt.year)]

    @classmethod
    def _angle_from_day_in_century(cls, dt: datetime) -> float:
        fraction = cls._day_in_decade(dt) / cls._days_in_decade[cls._decade_from_year(dt.year)]
        fraction += math.floor((dt.year - 2020) / 10)
        return 10 * fraction * cls._twopi / 170

@typechecked
class Calendar1:

    def __init__(self,
        side: int = 450,
        background_color: Union[Color, None] = None,
        foreground_color: Union[Color, None] = None,
    ):

        if background_color is None:
            background_color = Color(0, 0, 0)
        if foreground_color is None:
            foreground_color = Color(255, 0, 0)

        self._side = side
        self._background_color = background_color
        self._foreground_color = foreground_color

        self._center = Vector2D(self._side / 2, self._side / 2)
        self._factor = self._side / 450

        self._font_years = DrawingBoard.make_font("Oxygen Mono", 20.0 * self._factor)
        self._font_decades = DrawingBoard.make_font("Oxygen Mono", 8.0 * self._factor)
        self._font_date = DrawingBoard.make_font("Oxygen Mono", 38.0 * self._factor)

        self._background = self._draw_background()

    def __call__(self, dt: datetime) -> Image:

        foreground = _Foreground(
            width = self._side,
            height = self._side,
            offset = self._center,
            background_color = self._background_color.as_transparent(),
        )

        foreground.draw_text(
            text = dt.strftime('%Y-%m-%d'),
            point = Vector2D(0.0, 90.0 * self._factor),
            font = self._font_date,
            font_color = self._foreground_color,
        )

        foreground.draw_hands(
            dt = dt,
            factor = self._factor,
            color = self._foreground_color,
        )

        foreground = foreground.as_pil()

        image = new(
            'RGBA',
            (self._side, self._side),
            self._background_color.as_transparent().as_rgba_int(),
        ) # transparent black
        image.paste(im = self._background, mask = self._background)
        image.paste(im = foreground, mask = foreground)

        return image

    def _draw_background(self) -> Image:

        canvas = _Background(
            width = self._side,
            height = self._side,
            offset = self._center,
            background_color = self._background_color,
            )

        canvas.draw_ticks(
            r1 = 220.0 * self._factor,
            r2 = 203.0 * self._factor,
            ticks = range(0, 10 * 12),
            line_color = self._foreground_color,
            line_width = 2.0 * self._factor,
            ) # months in decade (outer minor ticks)
        canvas.draw_ticks(
            r1 = 220.0 * self._factor,
            r2 = 200.0 * self._factor,
            ticks = range(0, 10),
            line_color = self._foreground_color,
            line_width = 5.0 * self._factor,
            ) # years in decade (outer major ticks)
        canvas.draw_labels(
            r = 182 * self._factor,
            labels = [f'{year:d}' for year in range(10)],
            font = self._font_years,
            font_color = self._foreground_color,
        ) # years in decade (outer major ticks labels)

        canvas.draw_ticks(
            r1 = 150.0 * self._factor,
            r2 = 133.0 * self._factor,
            ticks = range(1970, 2070 + 1, 1),
            line_color = self._foreground_color,
            line_width = 1.0 * self._factor,
            zero = 2020,
            length = 170,
            ) # year in century (inner minor ticks)
        canvas.draw_ticks(
            r1 = 150.0 * self._factor,
            r2 = 130.0 * self._factor,
            ticks = range(1970, 2070 + 10, 10),
            line_color = self._foreground_color,
            line_width = 2.5 * self._factor,
            zero = 2020,
            length = 170,
            ) # decade in century (inner major ticks)
        labels = [f'{decade:d}' for decade in range(1970, 2070 + 10, 10)]
        canvas.draw_labels(
            r = 114 * self._factor,
            labels = labels,
            font = self._font_decades,
            font_color = self._foreground_color,
            zero = labels.index('2020'),
            length = 17,
        ) # decade in century (inner major ticks labels)

        return canvas.as_pil()
