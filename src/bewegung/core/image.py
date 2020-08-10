# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/image.py: Simple 2D cairo renderer

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

import io
import math
import typing

import cairo
import PIL.Image
from typeguard import typechecked

import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo

import IPython.display

from .abc import ImageABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _geometry(func: typing.Callable) -> typing.Callable:
    def wrapper(self, *args, **kwargs):
        self._ctx.save()
        self._ctx.new_path()
        ret = func(self, *args, **kwargs)
        self._ctx.restore()
        return ret
    return wrapper

@typechecked
class Image(ImageABC):

    def __init__(self,
        width: int,
        height: int,
        subpixels: int = 1,
        background_color: typing.Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 0.0),
        ):

        self._width, self._height, self._subpixels = width, height, subpixels

        self._surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            self._width * self._subpixels,
            self._height * self._subpixels,
            )
        if self._subpixels != 1:
             self._surface.set_device_scale(float(self._subpixels), float(self._subpixels))

        self._ctx = cairo.Context(self._surface)
        self._set_background_color(background_color)

    def as_pil(self) -> PIL.Image:

        if self._subpixels == 1:
            return PIL.Image.frombuffer(
                mode = 'RGBA',
                size = (self._width, self._height),
                data = self._surface.get_data(),
                )

        return PIL.Image.frombuffer(
            mode = 'RGBA',
            size = (self._width * self._subpixels, self._height * self._subpixels),
            data = self._surface.get_data(),
            ).resize(
                (self._width, self._height),
                resample = PIL.Image.LANCZOS,
            )

    def display(self):

        with io.BytesIO() as buffer:
            self.as_pil().save(buffer, format = 'PNG')
            image_bytes = buffer.getvalue()

        IPython.display.display(
            IPython.display.Image(data = image_bytes, format = 'png')
            )

    def save(self, fn: str):

        self._surface.write_to_png(fn)

    @_geometry
    def draw_text(self,
        text: str = '',
        x: float = 0.0, y: float = 0.0, angle: float = 0.0,
        font: typing.Union[Pango.FontDescription, None] = None,
        font_color: typing.Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 0.0),
        alignment: str = 'cc',
        ):

        if font is None:
            font = self.make_font('Arial', 10.0)

        layout = PangoCairo.create_layout(self._ctx)
        layout.set_font_description(font)
        layout.set_markup(text, -1)

        self._ctx.set_source_rgba(*font_color)

        _, text_extents = layout.get_pixel_extents()
        text_width, text_height = text_extents.width, text_extents.height

        self._ctx.translate(x, y)
        if angle != 0.0:
            self._ctx.rotate(angle)
        self._ctx.translate(*self._alignments[alignment](text_width, text_height))
        self._ctx.move_to(0, 0)

        PangoCairo.show_layout(self._ctx, layout)

    _alignments = {
        'tl': lambda width, height: (0.0, 0.0), # top left
        'tc': lambda width, height: (-width / 2, 0.0), # top center
        'tr': lambda width, height: (-width, 0.0), # top right
        'cl': lambda width, height: (0.0, -height / 2), # center left
        'cc': lambda width, height: (-width / 2, -height / 2), # center center
        'cr': lambda width, height: (-width, -height / 2), # center right
        'bl': lambda width, height: (0.0, -height), # bottom left
        'bc': lambda width, height: (-width / 2, -height), # bottom center
        'br': lambda width, height: (-width, -height), # bottom right
    }

    @staticmethod
    def make_font(family: str, size: float):

        return Pango.font_description_from_string(f'{family:s} {size:.2f}')

    @_geometry
    def draw_polygon(self,
        *points: typing.Tuple[float, float],
        **kwargs,
        ):

        assert len(points) >= 2
        self._ctx.move_to(*points[0])
        for point in points[1:]:
            self._ctx.line_to(*point)
        self._stroke(**kwargs)

    @_geometry
    def draw_circle(self,
        x: float = 0.0,
        y: float = 0.0,
        r: float = 1.0,
        **kwargs,
        ):

        self._ctx.arc(
            x, y, r,
            0, 2 * math.pi,
        )
        self._stroke(**kwargs)

    @_geometry
    def draw_filledcircle(self,
        x: float = 0.0,
        y: float = 0.0,
        r: float = 1.0,
        fill_color: typing.Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 0.0),
        ):

        self._ctx.arc(
            x, y, r,
            0, 2 * math.pi,
        )
        self._ctx.set_source_rgba(*fill_color)
        self._ctx.fill()

    def _stroke(self,
        line_color: typing.Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 0.0),
        line_width: float = 1.0,
        **kwargs,
        ):

        self._ctx.set_source_rgba(*line_color)
        self._ctx.set_line_width(line_width)
        self._ctx.stroke()

    def _set_background_color(self,
        fill_color: typing.Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 0.0),
        ):

        self._ctx.set_source_rgba(*fill_color)
        self._ctx.rectangle(0, 0, self._width, self._height)
        self._ctx.fill()
