# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/canvas/drawingboard/canvas.py: Backend Canvas

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

from PIL.Image import Image
from typeguard import typechecked

from .._base import CanvasBase
from ...abc import VideoABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Canvas(CanvasBase):

    def __init__(self):

        super().__init__()

        self._DrawingBoard = None

    def prototype(self, video: VideoABC, **kwargs) -> Callable:

        if not self._loaded:
            self.load()

        if 'width' not in kwargs.keys():
            kwargs['width'] = video.width
        if 'height' not in kwargs.keys():
            kwargs['height'] = video.height

        return lambda: self._DrawingBoard(**kwargs)

    def isinstance(self, obj: Any, hard: bool = True) -> bool:

        if not self._loaded and not hard:
            return False
        if not self._loaded:
            self.load()

        return isinstance(obj, self._DrawingBoard)

    def load(self):

        if self._loaded:
            return

        from .core import DrawingBoard

        self._DrawingBoard = DrawingBoard

        self._loaded = True

    def to_pil(self, obj: Any) -> Image:

        if not self._loaded:
            self.load()

        assert isinstance(obj, self._DrawingBoard)

        return obj.as_pil()

    @property
    def type(self) -> Type:

        if not self._loaded:
            self.load()

        return self._DrawingBoard
