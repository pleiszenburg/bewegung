# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_backends/datashader.py: Datashader backend

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
from PIL import ImageOps

from ...lib import typechecked
from .._abc import VideoABC
from ._base import BackendBase

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Backend(BackendBase):

    _name = 'Datashader'

    def __init__(self):

        super().__init__()

        self._DS_Image = None

    def _prototype(self, video: VideoABC, **kwargs) -> Callable:

        if 'plot_width' in kwargs.keys() and 'width' in kwargs.keys():
            kwargs.pop('width')
        if 'plot_height' in kwargs.keys() and 'height' in kwargs.keys():
            kwargs.pop('height')

        if 'plot_width' not in kwargs.keys() and 'width' in kwargs.keys():
            kwargs['plot_width'] = kwargs.pop('width')
        if 'plot_height' not in kwargs.keys() and 'height' in kwargs.keys():
            kwargs['plot_height'] = kwargs.pop('height')

        if 'plot_width' not in kwargs.keys():
            kwargs['plot_width'] = video.width
        if 'plot_height' not in kwargs.keys():
            kwargs['plot_height'] = video.height

        if 'x_range' not in kwargs.keys():
            kwargs['x_range'] = (0, video.width)
        if 'y_range' not in kwargs.keys():
            kwargs['y_range'] = (0, video.height)

        return lambda: self._type(**kwargs)

    def _isinstance(self, obj: Any) -> bool:

        return isinstance(obj, self._DS_Image) # Return type is not a canvas!

    def _load(self):

        from datashader import Canvas as DS_Canvas
        from datashader.transfer_functions import Image as DS_Image

        self._type = DS_Canvas
        self._DS_Image = DS_Image

    def _to_pil(self, obj: Any) -> Image:

        cvs = obj.to_pil()
        if cvs.mode != 'RGBA':
            raise TypeError('unhandled image mode')
        return ImageOps.flip(cvs) # datashader's y axis must be flipped
