# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/canvas/_base.py: Canvas base class

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

from ..abc import CanvasABC, VideoABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class CanvasBase(CanvasABC):

    def __init__(self):

        self._loaded = False

    def prototype(self, video: VideoABC, **kwargs) -> Callable:

        raise NotImplementedError()

    def isinstance(self, obj: Any, hard: bool = True) -> bool:

        raise NotImplementedError()

    def load(self):

        raise NotImplementedError()

    def to_pil(self, obj: Any) -> Image:

        raise NotImplementedError()

    @property
    def loaded(self) -> bool:

        return self._loaded

    @property
    def type(self) -> Type:

        raise NotImplementedError()
