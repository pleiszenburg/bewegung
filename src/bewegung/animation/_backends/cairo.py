# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_backends/cairo.py: Cairo backend

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

from typing import Any, Callable

from PIL.Image import Image, frombuffer, merge

from ...lib import typechecked
from .._abc import VideoABC
from ._base import BackendBase

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Backend(BackendBase):

    _name = 'Cairo'

    def __init__(self):

        super().__init__()

        self._FORMAT_ARGB32 = None
        self._Format = None

    def _prototype(self, video: VideoABC, **kwargs) -> Callable:

        if 'format' not in kwargs.keys():
            kwargs['format'] = self._FORMAT_ARGB32
        if 'width' not in kwargs.keys():
            kwargs['width'] = video.width
        if 'height' not in kwargs.keys():
            kwargs['height'] = video.height

        assert len(kwargs) == 3

        return lambda: self._type(kwargs['format'], kwargs['width'], kwargs['height'])

    def _load(self):

        from cairo import FORMAT_ARGB32, ImageSurface, Format

        self._type = ImageSurface

        self._FORMAT_ARGB32 = FORMAT_ARGB32
        self._Format = Format

    def _to_pil(self, obj: Any) -> Image:

        if obj.get_format() != self._Format.ARGB32:
            raise TypeError('ImageSurface uses unhandled format')

        image = frombuffer(
            mode = 'RGBa',
            size = (obj.get_width(), obj.get_height()),
            data = obj.get_data().tobytes(), # call to "tobytes" required because of RGBa mode
            )
        b, g, r, a = image.split()
        return merge('RGBa', (r, g, b, a)).convert("RGBA")
