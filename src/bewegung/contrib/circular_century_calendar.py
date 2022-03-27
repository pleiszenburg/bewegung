# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/contrib/circular_century_calendar.py: Circular Century Calendar

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

import calendar
from datetime import datetime
import math
from typing import List, Union

from PIL.Image import Image, new, LANCZOS

from ..lib import Color, typechecked
from ..drawingboard import DrawingBoard
from ..linalg import Matrix, Vector2D

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
        font: DrawingBoard.Pango.FontDescription,
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
                font_color = font_color,
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

        mr = Matrix.from_2d_rotation(self._angle_from_day_in_century(dt))
        self.draw_filledpolygon(
            mr @ (Vector2D(-7.0, -98.0) * factor),
            mr @ (Vector2D(0, -118.0) * factor),
            mr @ (Vector2D(7.0, -98.0) * factor),
            fill_color = color,
        ) # decade in century

        mr = Matrix.from_2d_rotation(self._angle_from_day_in_decade(dt))
        self.draw_filledpolygon(
            mr @ (Vector2D(-7.0, -160.0) * factor),
            mr @ (Vector2D(0, -180.0) * factor),
            mr @ (Vector2D(7.0, -160.0) * factor),
            fill_color = color,
        ) # year in decade

        mr = Matrix.from_2d_rotation(self._angle_from_day_in_year(dt))
        self.draw_filledcircle(
            point = mr @ (Vector2D(0.0, -218.0) * factor),
            r = 8,
            fill_color = color,
        )

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
class CircularCenturyCalendar:

    def __init__(self,
        side: int = 450,
        subpixels: int = 1,
        background_color: Union[Color, None] = None,
        foreground_color: Union[Color, None] = None,
    ):

        if background_color is None:
            background_color = Color(0, 0, 0)
        if foreground_color is None:
            foreground_color = Color(255, 0, 0)

        self._actual_side = side
        self._subpixels = subpixels
        self._background_color = background_color
        self._foreground_color = foreground_color

        self._side = self._actual_side * subpixels
        self._center = Vector2D(self._side / 2, self._side / 2)
        self._factor = self._side / 450

        self._font_years = DrawingBoard.make_font("Oxygen Mono", 20.0 * self._factor)
        self._font_decades = DrawingBoard.make_font("Oxygen Mono", 10.0 * self._factor)
        self._font_date = DrawingBoard.make_font("Oxygen Mono", 35.0 * self._factor)

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

        return image.resize(
            (self._actual_side, self._actual_side),
            resample = LANCZOS,
        )

    def _draw_background(self) -> Image:

        canvas = _Background(
            width = self._side,
            height = self._side,
            offset = self._center,
            background_color = self._background_color,
            )

        canvas.draw_ticks(
            r1 = 210.0 * self._factor,
            r2 = 193.0 * self._factor,
            ticks = range(0, 10 * 12),
            line_color = self._foreground_color,
            line_width = 2.0 * self._factor,
            ) # months in decade (outer minor ticks)
        canvas.draw_ticks(
            r1 = 210.0 * self._factor,
            r2 = 187.0 * self._factor,
            ticks = range(0, 10),
            line_color = self._foreground_color,
            line_width = 5.0 * self._factor,
            ) # years in decade (outer major ticks)
        canvas.draw_labels(
            r = 169 * self._factor,
            labels = [f'{year:d}' for year in range(10)],
            font = self._font_years,
            font_color = self._foreground_color,
        ) # years in decade (outer major ticks labels)

        canvas.draw_ticks(
            r1 = 145.0 * self._factor,
            r2 = 128.0 * self._factor,
            ticks = range(1970, 2070 + 2, 2),
            line_color = self._foreground_color,
            line_width = 1.0 * self._factor,
            zero = 2020,
            length = 170,
            ) # year in century (inner minor ticks)
        canvas.draw_ticks(
            r1 = 145.0 * self._factor,
            r2 = 124.0 * self._factor,
            ticks = range(1970, 2070 + 10, 10),
            line_color = self._foreground_color,
            line_width = 2.5 * self._factor,
            zero = 2020,
            length = 170,
            ) # decade in century (inner major ticks)
        labels = [f'{decade:d}' for decade in range(1970, 2070 + 10, 10)]
        canvas.draw_labels(
            r = 102 * self._factor,
            labels = labels,
            font = self._font_decades,
            font_color = self._foreground_color,
            zero = labels.index('2020'),
            length = 17,
        ) # decade in century (inner major ticks labels)

        return canvas.as_pil()
