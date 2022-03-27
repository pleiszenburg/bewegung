# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/drawingboard/_core.py: Simple 2D cairo renderer

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

from functools import wraps
import io
import math
import os
from typing import Callable, Union

import cairo
from PIL import Image

try:
    import gi
    gi.require_version('Pango', '1.0')
    gi.require_version('PangoCairo', '1.0')
    gi.require_version('Rsvg', '2.0')
    from gi.repository import Pango, PangoCairo, Rsvg
except Exception as e:
    if os.environ.get('RTD_NO_GI', 'False') == 'True': # catch ReadTheDocs builds
        class Pango:
            class Alignment:
                LEFT, CENTER, RIGHT = None, None, None
            class FontDescription:
                pass
        PangoCairo = None
        class Rsvg:
            class Handle:
                pass
    else:
        raise e

try:
    import IPython.display
except ModuleNotFoundError:
    IPython = None

from ..lib import Color, typechecked
from ..linalg import Vector2D, Matrix
from ._abc import DrawingBoardABC

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
    """
    A wrapper around Cairo, Pango (PangoCairo) and Rsvg, providing a canvas with a simple API for day-to-day drawing tasks.

    DrawingBoard objects are mutable. The color mode is 32 bit RGBA (actually cairo's ARGB32).

    Args:
        width : Canvas width in pixels
        height : Canvas width in pixels
        offset : Center of coordinate system (device offset)
        subpixels : Number of subpixels per pixel (devise scale)
        background_color : Canvas background color - transparent white by default
    """

    cairo = cairo
    Pango = Pango
    PangoCairo = PangoCairo
    Rsvg = Rsvg

    def __init__(self,
        width: int,
        height: int,
        offset: Union[Vector2D, None] = None,
        subpixels: int = 1,
        background_color: Union[Color, None] = None,
        ):

        if width < 1:
            raise ValueError('width must be at least 1 pixel')
        if height < 1:
            raise ValueError('height must be at least 1 pixel')
        if subpixels < 1:
            raise ValueError('there must be a positive number subpixels')

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

        if self._offset != Vector2D(0.0, 0.0):
            self._surface.set_device_offset(self._offset.x * self._subpixels, self._offset.y * self._subpixels)

        if self._subpixels != 1:
            self._surface.set_device_scale(float(self._subpixels), float(self._subpixels))

        self._ctx = cairo.Context(self._surface)
        self._set_background_color(background_color)

    def __repr__(self) -> str:

        return f'<DrawingBoard width={self._width:d} height={self._height:d} subpixels={self._subpixels:d}>'

    def as_pil(self) -> Image.Image:
        """
        Exports drawing as a Pillow Image object
        """

        if self._subpixels == 1:
            return self.swap_channels(Image.frombuffer(
                mode = 'RGBa',
                size = (self._width, self._height),
                data = self._surface.get_data().tobytes(), # call to "tobytes" required because of RGBa mode
                )).convert("RGBA")

        return self.swap_channels(Image.frombuffer(
            mode = 'RGBa',
            size = (self._width * self._subpixels, self._height * self._subpixels),
            data = self._surface.get_data().tobytes(), # call to "tobytes" required because of RGBa mode
            ).convert("RGBA").resize(
                (self._width, self._height),
                resample = Image.LANCZOS,
            ))

    @staticmethod
    def swap_channels(image: Image.Image) -> Image.Image:

        b, g, r, a = image.split()
        return Image.merge(image.mode, (r, g, b, a))

    def display(self):
        """
        Displays drawing in an IPython console or Jupyter notebook
        """

        if IPython is None:
            raise NotImplementedError('IPython is not available')

        with io.BytesIO() as buffer:
            self.as_pil().save(buffer, format = 'PNG')
            image_bytes = buffer.getvalue()

        IPython.display.display(
            IPython.display.Image(data = image_bytes, format = 'png')
            )

    def save(self, fn: str):
        """
        Saves drawing to a file

        Args:
            fn : Path to image file. The image format is derived from the file extension.
        """

        if len(fn) == 0:
            raise ValueError('filename must not be empty')

        self.as_pil().save(fn)

    @_geometry
    def draw_svg(self,
        fn: Union[str, None] = None,
        raw: Union[bytes, None] = None,
        svg: Union[Rsvg.Handle, None] = None,
        point: Union[Vector2D, None] = None,
        scale: float = 1.0,
        angle: float = 0.0,
        anchor: Union[Vector2D, str] = 'cc',
    ):
        """
        Adds an SVG to the drawing.

        The SVG can be provided with one of the three following options:

        (1) a path/filename, from where the SVG can be loaded
        (2) a raw sequence of bytes containing the SVG markup
        (3) a handle on an rsvg object

        Args:
            fn : Path to SVG file (1)
            raw : SVG markup (2)
            svg : rsvg handle object (3)
            point : Location of the SVG within the drawing relative to the SVG's anchor
            scale : Allows to resize the SVG by the provided factor
            angle : Rotates the SVG by a given angle in radians
            anchor : Describes the achor point of the SVG.
                The location an either be provided as a 2D vector or as a two-letter code.
                First letters can be "t" (top), "c" (center) and "b" (bottom).
                Second letters can be "l" (left), "c" (center) and "r" (right).
        """

        if not ((fn is not None) ^ (raw is not None) ^ (svg is not None)):
            raise RuntimeError('SVG must be provided exactly once')

        if svg is None:
            if raw is None:
                if len(fn) == 0:
                    raise ValueError('filename must not be empty')
                svg = Rsvg.Handle.new_from_file(fn)
            else:
                svg = Rsvg.Handle.new_from_data(raw)

        if point is None:
            point = Vector2D(0.0, 0.0)
        scale = Vector2D(scale, scale)

        svg_dim = svg.get_dimensions()
        svg_dim = Vector2D(svg_dim.width, svg_dim.height)

        if isinstance(anchor, str):
            try:
                anchor = self._anchor[anchor]
            except KeyError:
                raise ValueError('unknown anchor point')
            anchor = anchor(*svg_dim.as_tuple())
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
    def make_svg(
        fn: Union[str, None] = None,
        raw: Union[bytes, None] = None,
        ) -> Rsvg.Handle:
        """
        Generates an rsvg handle for re-use.

        The SVG's data can be provided with one of the two following options:

        (1) a path/filename, from where the SVG can be loaded
        (2) a raw sequence of bytes containing the SVG markup

        Args:
            fn : Path to SVG file (1)
            raw : SVG markup (2)
        """

        if not ((fn is not None) ^ (raw is not None)):
            raise RuntimeError('SVG must be provided exactly once')

        if raw is not None:
            return Rsvg.Handle.new_from_data(raw)

        if len(fn) == 0:
            raise ValueError('filename must not be empty')
        return Rsvg.Handle.new_from_file(fn)

    @_geometry
    def draw_text(self,
        text: str = '',
        point: Union[Vector2D, None] = None,
        angle: float = 0.0,
        font: Union[Pango.FontDescription, None] = None,
        font_color: Union[Color, None] = None,
        alignment: str = 'l',
        anchor: Union[Vector2D, str] = 'cc',
        ):
        """
        Adds text to the drawing.

        Args:
            text : The actual text. Can handle explicit line breaks (``\\n``) but does not offer automatic line breaks.
            point : Location of the text within the drawing relative to the text's anchor
            angle : Rotates the text by a given angle in radians
            font : A Pango font description object
            font_color : The font color. Opaque black by default.
            alignment : Single letter describing the text allignment. Can be "l" (left), "c" (center) and "r" (right).
            anchor : Describes the achor point of the text.
                The location an either be provided as a 2D vector or as a two-letter code.
                First letters can be "t" (top), "c" (center) and "b" (bottom).
                Second letters can be "l" (left), "c" (center) and "r" (right).
        """

        if point is None:
            point = Vector2D(0.0, 0.0)
        if font is None:
            font = self.make_font('Arial', 10.0)
        if font_color is None:
            font_color = Color(0, 0, 0, 255) # opaque black

        layout = PangoCairo.create_layout(self._ctx)
        layout.set_font_description(font)
        try:
            alignment = self._alignment[alignment]
        except KeyError:
            raise ValueError('unknown alignment')
        layout.set_alignment(alignment)
        layout.set_markup(text, -1)

        self._ctx.set_source_rgba(*font_color.as_rgba_float())

        if isinstance(anchor, str):
            _, text_extents = layout.get_pixel_extents()
            try:
                anchor = self._anchor[anchor]
            except KeyError:
                raise ValueError('unknown anchor point')
            anchor = anchor(text_extents.width, text_extents.height)
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
        'tr': lambda width, height: Vector2D(float(-width), 0.0), # top right
        'cl': lambda width, height: Vector2D(0.0, -height / 2), # center left
        'cc': lambda width, height: Vector2D(-width / 2, -height / 2), # center center
        'cr': lambda width, height: Vector2D(float(-width), -height / 2), # center right
        'bl': lambda width, height: Vector2D(0.0, float(-height)), # bottom left
        'bc': lambda width, height: Vector2D(-width / 2, float(-height)), # bottom center
        'br': lambda width, height: Vector2D(float(-width), float(-height)), # bottom right
    }
    _alignment = {
        'l': Pango.Alignment.LEFT,
        'c': Pango.Alignment.CENTER,
        'r': Pango.Alignment.RIGHT,
    }

    @staticmethod
    def make_font(family: str, size: float) -> Pango.FontDescription:
        """
        Generates a Pango font description for re-use.

        Args:
            family : Font family (name)
            size : Font size
        """

        # TODO https://developer.gnome.org/pango/stable/pango-Fonts.html#pango-font-description-from-string
        return Pango.font_description_from_string(f'{family:s} {size:.2f}')

    @_geometry
    def draw_polygon(self,
        *points: Vector2D,
        close: bool = False,
        **kwargs,
        ):
        """
        Adds an unfilled polygon to the drawing.

        Args:
            points : An arbitrary number of 2D vectors
            close : Whether or not the polygon should be closed
            kwargs : Arguments for line stroke (see ``_stroke``)
        """

        if len(points) < 2:
            raise ValueError('at least two points most be provided')

        self._ctx.move_to(points[0].x, points[0].y)
        for point in points[1:]:
            self._ctx.line_to(point.x, point.y)
        if close:
            self._ctx.line_to(points[0].x, points[0].y)
        self._stroke(**kwargs)

    @_geometry
    def draw_filledpolygon(self,
        *points: Vector2D,
        fill_color: Union[Color, None] = None,
        ):
        """
        Adds a filled, frame-less polygon to the drawing.

        Args:
            points : An arbitrary number of 2D vectors
            fill_color : Fill color. Opaque black by default.
        """

        if len(points) < 3:
            raise ValueError('at least three points most be provided')
        if fill_color is None:
            fill_color = Color(0, 0, 0, 255) # opaque black

        self._ctx.move_to(points[0].x, points[0].y)
        for point in points[1:]:
            self._ctx.line_to(point.x, point.y)
        self._ctx.set_source_rgba(*fill_color.as_rgba_float())
        self._ctx.fill()

    @_geometry
    def draw_bezier(self,
        a: Vector2D,
        b: Vector2D,
        c: Vector2D,
        d: Vector2D,
        **kwargs,
        ):
        """
        Adds a bezier curve to the drawing.

        Args:
            a : A 2D vector representing P0
            b : A 2D vector representing P1
            c : A 2D vector representing P2
            d : A 2D vector representing P3
            kwargs : Arguments for line stroke (see ``_stroke``)
        """

        self._ctx.move_to(a.x, a.y)
        self._ctx.curve_to(b.x, b.y, c.x, c.y, d.x, d.y)
        self._stroke(**kwargs)

    @_geometry
    def draw_circle(self,
        point: Vector2D,
        r: float = 1.0,
        **kwargs,
        ):
        """
        Adds an unfilled circle to the drawing.

        Args:
            point : Center of circle
            r : Radius of circle
            kwargs : Arguments for line stroke (see ``_stroke``)
        """

        if r < 0:
            raise ValueError('radius must be greater or equal to zero')

        self._ctx.arc(
            point.x, point.y, r,
            0, 2 * math.pi,
        )
        self._stroke(**kwargs)

    @_geometry
    def draw_filledcircle(self,
        point: Vector2D,
        r: float = 1.0,
        fill_color: Union[Color, None] = None,
        ):
        """
        Adds a filled, frame-less circle to the drawing.

        Args:
            point : Center of circle
            r : Radius of circle
            fill_color : Fill color. Opaque black by default.
        """

        if r < 0:
            raise ValueError('radius must be greater or equal to zero')

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
        """
        Strokes lines. Never called directly.

        Args:
            line_color : Color of line. Opaque black by default.
            line_width : Width of line
        """

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
        """
        Exposes drawing's cairo.Context object
        """

        return self._ctx

    @property
    def surface(self) -> cairo.ImageSurface:
        """
        Exposes drawing's cairo.ImageSurface object
        """

        return self._surface

    @property
    def width(self) -> int:
        """
        Width of canvas
        """

        return self._width

    @property
    def height(self) -> int:
        """
        Height of canvas
        """

        return self._height
