# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_backends/matplotlib.py: Matplotlib backend

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

from numbers import Number
from typing import Any, Callable
import warnings

from PIL.Image import Image, fromarray, frombuffer, merge

from ...lib import Color, typechecked
from .._abc import VideoABC
from ._base import BackendBase

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Backend(BackendBase):

    _name = 'Matplotlib'

    def __init__(self):

        super().__init__()

        self._plt, self._Figure = None, None

        self._mplcairo_present = False

    def _prototype(self, video: VideoABC, **kwargs) -> Callable:

        if 'dpi' not in kwargs.keys():
            kwargs['dpi'] = 300 # important!
        if 'figsize' not in kwargs.keys():
            if 'width' not in kwargs.keys():
                kwargs['width'] = video.width
            if 'height' not in kwargs.keys():
                kwargs['height'] = video.height
            assert isinstance(kwargs['width'], Number)
            assert isinstance(kwargs['height'], Number)
            kwargs['figsize'] = (
                kwargs.pop('width') / kwargs['dpi'],
                kwargs.pop('height') / kwargs['dpi'],
            ) # inch

        if 'background_color' in kwargs.keys() and 'facecolor' in kwargs.keys():
            kwargs.pop('background_color')
        if 'background_color' in kwargs.keys():
            if not isinstance(kwargs['background_color'], Color):
                raise TypeError('color expected')
            kwargs['facecolor'] = f'#{kwargs.pop("background_color").as_hex():s}'
        if 'facecolor' not in kwargs.keys():
            kwargs['facecolor'] = '#FFFFFF00'

        if 'tight_layout' not in kwargs.keys():
            kwargs['tight_layout'] = True

        managed = kwargs.pop('managed') if 'managed' in kwargs.keys() else True
        assert isinstance(managed, bool)

        @typechecked
        def new_figure() -> self._Figure:
            fig = self._type(**kwargs)
            if managed:
                setattr(fig, '__bewegung_managed__', None) # flag: close figure after extracting image
            return fig

        return new_figure

    def _isinstance(self, obj: Any) -> bool:

        return isinstance(obj, self._Figure) # Return type is a Figure object!

    def _load(self):

        try:
            import mplcairo.base # import before matplotlib
            self._mplcairo_present = True
        except ModuleNotFoundError:
            warnings.warn('`mplcairo` matplotlib backend is not installed, falling back to `cairo`')

        import matplotlib
        matplotlib.use(
            "module://mplcairo.base" if self._mplcairo_present else "cairo",
            force = True,
        ) # use mplcairo.base as non-GUI backend

        import matplotlib.pyplot as plt # import pyplot last
        from matplotlib.figure import Figure

        self._type = plt.figure

        self._plt = plt
        self._Figure = Figure

    def _to_pil(self, obj: Any) -> Image:

        if self._mplcairo_present:

            obj.canvas.draw()

            buffer = obj.canvas.renderer.buffer_rgba()
            assert buffer.dtype.name == 'uint8' # TODO cairo & mplcairo also support RGBA128F

            image = fromarray(buffer) # depends on matplotlib backend - https://stackoverflow.com/q/57316491/1672565

        else:

            surface = obj.canvas._get_printed_image_surface() # returns ARGB32 cairo surface

            image = frombuffer(
                mode = 'RGBa',
                size = (surface.get_width(), surface.get_height()),
                data = surface.get_data().tobytes(), # call to "tobytes" required because of RGBa mode
                )
            b, g, r, a = image.split()
            image = merge('RGBa', (r, g, b, a)).convert("RGBA")

        if hasattr(obj, '__bewegung_managed__'): # close flagged image
            self._plt.close(obj)

        assert image.mode == 'RGBA'

        return image
