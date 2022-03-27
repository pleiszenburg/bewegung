# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_backends/pillow.py: Pillow backend

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

from PIL.Image import Image, new

from ...lib import Color, typechecked
from .._abc import VideoABC
from ._base import BackendBase

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Backend(BackendBase):

    _name = 'Pillow'

    def _prototype(self, video: VideoABC, **kwargs) -> Callable:

        if 'mode' not in kwargs.keys():
            kwargs['mode'] = 'RGBA'

        if 'size' in kwargs.keys() and 'width' in kwargs.keys():
            kwargs.pop('width')
        if 'size' in kwargs.keys() and 'height' in kwargs.keys():
            kwargs.pop('height')
        if 'size' not in kwargs.keys():
            kwargs['size'] = (video.width, video.height)
        else:
            if 'width' not in kwargs.keys() and 'height' not in kwargs.keys():
                raise ValueError('width or height missing')
            kwargs['size'] = (kwargs.pop('width'), kwargs.pop('height'))

        if 'color' in kwargs.keys() and 'background_color' in kwargs.keys():
            kwargs.pop('background_color')
        if 'background_color' in kwargs.keys():
            if not isinstance(kwargs['background_color'], Color):
                raise TypeError('color expected')
            kwargs['color'] = kwargs.pop("background_color").as_rgba_int()

        return lambda: new(**kwargs)

    def _load(self):

        self._type = Image

    def _to_pil(self, obj: Any) -> Image:

        if obj.mode != 'RGBA':
            raise TypeError('unhandled image mode')

        return obj
