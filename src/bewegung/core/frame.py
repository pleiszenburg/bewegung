# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/frame.py: About video frames

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

import typing

import datashader
from typeguard import typechecked

from .abc import FrameSizeABC, IndexPoolABC
from .image import Image

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: ZIndexPool
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class IndexPool(IndexPoolABC):
    """
    Used to manage z-index values and preparation taks between layers. index-values are unique.
    """
    def __init__(self):
        self._pool = set()
    def __repr__(self) -> str:
        return f'<ZIndexPool len={len(self):d}>'
    def __contains__(self, index: int) -> bool:
        return index in self._pool
    def __len__(self) -> int:
        return len(self._pool)
    @property
    def max(self) -> int:
        return max(self._pool)
    @property
    def min(self) -> int:
        return min(self._pool)
    def as_list(self) -> typing.List[int]:
        return list(self._pool)
    def register_ontop(self) -> typing.Callable:
        index = (self.max + 1) if len(self) != 0 else 0
        self._pool.add(index)
        def decorator(func: typing.Callable) -> typing.Callable:
            def wrapper(*args, **kwargs):
                return index, lambda: func(*args, **kwargs)
            return wrapper
        return decorator
    def register_onbottom(self) -> typing.Callable:
        index = (self.min - 1) if len(self) != 0 else 0
        self._pool.add(index)
        def decorator(func: typing.Callable) -> typing.Callable:
            def wrapper(*args, **kwargs):
                return index, lambda: func(*args, **kwargs)
            return wrapper
        return decorator
    def register_custom(self, index: int) -> typing.Callable:
        if index in self:
            raise IndexError()
        self._pool.add(index)
        def decorator(func: typing.Callable) -> typing.Callable:
            def wrapper(*args, **kwargs):
                return index, lambda: func(*args, **kwargs)
            return wrapper
        return decorator

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: FrameSize
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class FrameSize(FrameSizeABC):
    """
    Simple wrapper for video frame size information
    """
    def __init__(self, width: int, height: int):
        if width <= 0:
            raise ValueError()
        if height <= 0:
            raise ValueError()
        self._width, self._height = width, height
    @property
    def w(self) -> int:
        return self._width
    @property
    def h(self) -> int:
        return self._height
    def create_image(self,
        background_color: typing.Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0),
        subpixels: int = 1,
        ) -> Image:
        return Image(
            self.w, self.h,
            background_color = background_color,
            subpixels = subpixels,
            )
    def create_dscanvas(self,
        x_range: typing.Union[None, typing.Tuple[int, int]] = None,
        y_range: typing.Union[None, typing.Tuple[int, int]] = None,
        ) -> datashader.Canvas:
        return datashader.Canvas(
            plot_width = self.w,
            plot_height = self.h,
            x_range = (0, self.w) if x_range is None else x_range,
            y_range = (0, self.h) if y_range is None else y_range,
            )
