# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/canvas/cairo.py: Cairo canvas

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

from typing import Any, Callable, Type

from PIL.Image import Image, frombuffer, merge
from typeguard import typechecked

from ._base import CanvasBase
from ..abc import VideoABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Canvas(CanvasBase):

    def __init__(self):

        super().__init__()

        self._FORMAT_ARGB32 = None
        self._ImageSurface = None
        self._Format = None

    def prototype(self, video: VideoABC, **kwargs) -> Callable:

        if not self._loaded:
            self.load()

        if 'format' not in kwargs.keys():
            kwargs['format'] = self._FORMAT_ARGB32
        if 'width' not in kwargs.keys():
            kwargs['width'] = video.width
        if 'height' not in kwargs.keys():
            kwargs['height'] = video.height

        assert len(kwargs) == 3

        return lambda: self._ImageSurface(kwargs['format'], kwargs['width'], kwargs['height'])

    def isinstance(self, obj: Any, hard: bool = True) -> bool:

        if not self._loaded and not hard:
            return False
        if not self._loaded:
            self.load()

        return isinstance(obj, self._ImageSurface)

    def load(self):

        if self._loaded:
            return

        from cairo import FORMAT_ARGB32, ImageSurface, Format

        self._FORMAT_ARGB32 = FORMAT_ARGB32
        self._ImageSurface = ImageSurface
        self._Format = Format

        self._loaded = True

    def to_pil(self, obj: Any) -> Image:

        if not self._loaded:
            self.load()

        assert isinstance(obj, self._ImageSurface)
        assert obj.get_format() == self._Format.ARGB32

        image = frombuffer(
            mode = 'RGBA',
            size = (obj.get_width(), obj.get_height()),
            data = obj.get_data(),
            )
        b, g, r, a = image.split()
        return merge('RGBA', (r, g, b, a))

    @property
    def type(self) -> Type:

        if not self._loaded:
            self.load()

        return self._ImageSurface
