# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_backends/drawingboard.py: Simple 2D cairo renderer

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

from PIL.Image import Image

from ...lib import typechecked
from .._abc import VideoABC
from ._base import BackendBase

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Backend(BackendBase):

    _name = 'DrawingBoard'

    def _prototype(self, video: VideoABC, **kwargs) -> Callable:

        if 'width' not in kwargs.keys():
            kwargs['width'] = video.width
        if 'height' not in kwargs.keys():
            kwargs['height'] = video.height

        return lambda: self._type(**kwargs)

    def _load(self):

        from ...drawingboard import DrawingBoard

        self._type = DrawingBoard

    def _to_pil(self, obj: Any) -> Image:

        image = obj.as_pil()

        assert image.mode == 'RGBA'

        return image
