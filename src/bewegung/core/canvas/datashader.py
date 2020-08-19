# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/canvas/datashader.py: Datashader canvas

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

from typing import Any, Callable

from datashader import Canvas as DS_Canvas
from datashader.transfer_functions import Image as DS_Image
from PIL.Image import Image
from PIL import ImageOps
from typeguard import typechecked

from ._base import CanvasBase
from ..abc import VideoABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Canvas(CanvasBase):

    def prototype(self, video: VideoABC, **kwargs) -> Callable:

        if 'plot_width' not in kwargs.keys():
            kwargs['plot_width'] = video.width
        if 'plot_height' not in kwargs.keys():
            kwargs['plot_height'] = video.height

        if 'x_range' not in kwargs.keys():
            kwargs['x_range'] = (0, video.width)
        if 'y_range' not in kwargs.keys():
            kwargs['y_range'] = (0, video.height)

        return lambda: DS_Canvas(**kwargs)

    def isinstance(self, obj: Any) -> bool:

        return isinstance(obj, DS_Image)

    def to_pil(self, obj: DS_Image) -> Image:

        cvs = obj.to_pil()
        assert cvs.mode == 'RGBA'
        return ImageOps.flip(cvs) # datashader's y axis must be flipped
