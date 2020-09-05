# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/drawingboard.py: Simple 2D cairo renderer

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

from functools import wraps
import io
import math
from typing import Callable, Union

import cairo
from PIL import Image
from typeguard import typechecked

import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
gi.require_version('Rsvg', '2.0')
from gi.repository import Pango, PangoCairo, Rsvg

import IPython.display

from .abc import DrawingBoardABC, Vector2DABC
from .color import Color
from .vector import Vector2D, Matrix

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _geometry(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.ctx.save()
        self.ctx.new_path()
        ret = func(self, *args, **kwargs)
        self.ctx.restore()
        return ret
    return wrapper

@typechecked
class DrawingBoard(DrawingBoardABC):

    def __init__(self,
        width: int,
        height: int,
        offset: Union[Vector2D, None] = None,
        subpixels: int = 1,
        background_color: Union[Color, None] = None,
        ):

        if offset is None:
            offset = Vector2D(0.0, 0.0)
        if background_color is None:
            background_color = Color(255, 255, 255, 0) # transparent white

        self._width, self._height, self._subpixels, self._offset = width, height, subpixels, offset

        self._surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            self._width * self._subpixels,
            self._height * self._subpixels,
            )
        if self._subpixels != 1:
            self._surface.set_device_scale(float(self._subpixels), float(self._subpixels))

        self._ctx = cairo.Context(self._surface)
        self._set_background_color(background_color)

        if self._offset != Vector2D(0.0, 0.0):
            self._surface.set_device_offset(*self._offset.as_tuple())

    def __repr__(self) -> str:
        return f'<DrawingBoard width={self._width:d} height={self._height:d} subpixels={self._subpixels:d}>'

    def as_pil(self) -> Image.Image:

        if self._subpixels == 1:
            return self.swap_channels(Image.frombuffer(
                mode = 'RGBA',
                size = (self._width, self._height),
                data = self._surface.get_data(),
                ))

        return self.swap_channels(Image.frombuffer(
            mode = 'RGBA',
            size = (self._width * self._subpixels, self._height * self._subpixels),
            data = self._surface.get_data(),
            ).resize(
                (self._width, self._height),
                resample = Image.LANCZOS,
            ))

    @staticmethod
    def swap_channels(image: Image.Image) -> Image.Image:

        b, g, r, a = image.split()
        return Image.merge('RGBA', (r, g, b, a))

    def display(self):

        with io.BytesIO() as buffer:
            self.as_pil().save(buffer, format = 'PNG')
            image_bytes = buffer.getvalue()

        IPython.display.display(
            IPython.display.Image(data = image_bytes, format = 'png')
            )

    def save(self, fn: str):

        self.as_pil().save(fn)

    @_geometry
    def draw_svg(self,
        fn: Union[str, None] = None,
        raw: Union[bytes, None] = None,
        svg: Union[Rsvg.Handle, None] = None,
        point: Union[Vector2DABC, None] = None,
        scale: float = 1.0,
        angle: float = 0.0,
        anchor: Union[Vector2D, str] = 'cc',
    ):

        assert (fn is not None) ^ (raw is not None) ^ (svg is not None)

        if svg is None:
            if raw is None:
                with open(fn, 'rb') as f:
                    raw = f.read()
                svg = Rsvg.Handle.new_from_data(raw)
            else:
                svg = Rsvg.Handle.new_from_file(fn)

        if point is None:
            point = Vector2D(0.0, 0.0)
        scale = Vector2D(scale, scale)

        svg_dim = svg.get_dimensions()
        svg_dim = Vector2D(svg_dim.width, svg_dim.height)

        if isinstance(anchor, str):
            anchor = self._anchor[anchor](*svg_dim.as_tuple())
        else:
            anchor = anchor * -1.0

        self._ctx.translate(
            point.x + anchor.x * scale.x,
            point.y + anchor.y * scale.y,
        )
        self._ctx.scale(*scale.as_tuple())
        self._ctx.rotate(angle)

        anchor = anchor * -1.0
        shift = Matrix.from_2d_rotation(-angle) @ anchor - anchor
        self._ctx.translate(*shift.as_tuple())

        svg.render_cairo(self._ctx)

    @staticmethod
    def make_svg(fn: str) -> Rsvg.Handle:

        return Rsvg.Handle.new_from_file(fn)

    @_geometry
    def draw_text(self,
        text: str = '',
        point: Union[Vector2DABC, None] = None,
        angle: float = 0.0,
        font: Union[Pango.FontDescription, None] = None,
        font_color: Union[Color, None] = None,
        alignment: str = 'l',
        anchor: Union[Vector2D, str] = 'cc',
        ):

        if point is None:
            point = Vector2D(0.0, 0.0)
        if font is None:
            font = self.make_font('Arial', 10.0)
        if font_color is None:
            font_color = Color(0, 0, 0, 255) # opaque black

        layout = PangoCairo.create_layout(self._ctx)
        layout.set_font_description(font)
        layout.set_alignment(self._alignment[alignment])
        layout.set_markup(text, -1)

        self._ctx.set_source_rgba(*font_color.as_rgba_float())

        if isinstance(anchor, str):
            _, text_extents = layout.get_pixel_extents()
            anchor = self._anchor[anchor](text_extents.width, text_extents.height)
        else:
            anchor = anchor * -1

        self._ctx.translate(point.x, point.y)
        if angle != 0.0:
            self._ctx.rotate(angle)
        self._ctx.translate(*anchor.as_tuple())
        self._ctx.move_to(0, 0)

        PangoCairo.show_layout(self._ctx, layout)

    _anchor = {
        'tl': lambda width, height: Vector2D(0.0, 0.0), # top left
        'tc': lambda width, height: Vector2D(-width / 2, 0.0), # top center
        'tr': lambda width, height: Vector2D(-width, 0.0), # top right
        'cl': lambda width, height: Vector2D(0.0, -height / 2), # center left
        'cc': lambda width, height: Vector2D(-width / 2, -height / 2), # center center
        'cr': lambda width, height: Vector2D(-width, -height / 2), # center right
        'bl': lambda width, height: Vector2D(0.0, -height), # bottom left
        'bc': lambda width, height: Vector2D(-width / 2, -height), # bottom center
        'br': lambda width, height: Vector2D(-width, -height), # bottom right
    }
    _alignment = {
        'l': Pango.Alignment.LEFT,
        'c': Pango.Alignment.CENTER,
        'r': Pango.Alignment.RIGHT,
    }

    @staticmethod
    def make_font(family: str, size: float) -> Pango.FontDescription:

        # TODO https://developer.gnome.org/pango/stable/pango-Fonts.html#pango-font-description-from-string
        return Pango.font_description_from_string(f'{family:s} {size:.2f}')

    @_geometry
    def draw_polygon(self,
        *points: Vector2DABC,
        **kwargs,
        ):

        assert len(points) > 1
        self._ctx.move_to(points[0].x, points[0].y)
        for point in points[1:]:
            self._ctx.line_to(point.x, point.y)
        self._stroke(**kwargs)

    @_geometry
    def draw_circle(self,
        point: Vector2DABC,
        r: float = 1.0,
        **kwargs,
        ):

        self._ctx.arc(
            point.x, point.y, r,
            0, 2 * math.pi,
        )
        self._stroke(**kwargs)

    @_geometry
    def draw_filledcircle(self,
        point: Vector2DABC,
        r: float = 1.0,
        fill_color: Union[Color, None] = None,
        ):

        if fill_color is None:
            fill_color = Color(0, 0, 0, 255) # opaque black

        self._ctx.arc(
            point.x, point.y, r,
            0, 2 * math.pi,
        )
        self._ctx.set_source_rgba(*fill_color.as_rgba_float())
        self._ctx.fill()

    def _stroke(self,
        line_color: Union[Color, None] = None,
        line_width: float = 1.0,
        **kwargs,
        ):

        if line_color is None:
            line_color = Color(0, 0, 0, 255) # opaque black

        self._ctx.set_source_rgba(*line_color.as_rgba_float())
        self._ctx.set_line_width(line_width)
        self._ctx.stroke()

    def _set_background_color(self,
        fill_color: Union[Color, None] = None,
        ):

        if fill_color is None:
            fill_color = Color(255, 255, 255, 0) # transparent white

        self._ctx.set_source_rgba(*fill_color.as_rgba_float())
        self._ctx.rectangle(0, 0, self._width, self._height)
        self._ctx.fill()

    @property
    def ctx(self) -> cairo.Context:
        return self._ctx

    @property
    def surface(self) -> cairo.ImageSurface:
        return self._surface
