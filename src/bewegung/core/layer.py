# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/layer.py: Layer function/method wrapper

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

from types import MethodType
from typing import Any, Callable, Union

from PIL import Image as PIL_Image
from typeguard import typechecked

from .abc import EffectABC, LayerABC, SequenceABC, TimeABC, VideoABC, Vector2DABC
from .canvas import inventory
from .vector import Vector2D

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Layer(LayerABC):
    """
    Mutable. Callable Layer Function/Method Wrapper, handling effects
    """

    def __init__(self,
        method: Callable,
        zindex: int,
        video: VideoABC,
        canvas: Union[Callable, None] = None,
        offset: Union[Vector2DABC, None] = None,
    ):

        if offset is None:
            offset = Vector2D(0, 0)

        self._method = method
        self._zindex_tag = zindex
        self._video = video
        self._canvas = self._video.canvas() if canvas is None else canvas
        self._offset = offset
        self._effects = []

        self._args = self._method.__code__.co_varnames[
            1:self._method.__code__.co_argcount # excluding self and internal namespace
            ] # parameters requested by user

    def __repr__(self) -> str:

        return f'<Layer name={self._method.__name__:s} zindex={self._zindex_tag:d}>'

    def __call__(self, sequence: SequenceABC, time: TimeABC) -> PIL_Image.Image:

        kwargs = {}
        cvs_start = None

        for param in self._args:
            if param == 'time':
                kwargs[param] = time
            elif param == 'reltime':
                kwargs[param] = time - sequence.start
            elif param == 'canvas':
                kwargs[param] = self._canvas()
                cvs_start = kwargs[param]
            else:
                raise ValueError('unknown parameter')

        cvs = self._method(sequence, **kwargs)
        if cvs is None:
            if cvs_start is not None:
                cvs = cvs_start
            else:
                raise ValueError('layer is missing a canvas')
        cvs = self._to_pil(cvs)

        for effect in self._effects:
            cvs = effect.apply_(
                cvs = cvs,
                video = self._video,
                sequence = sequence,
                time = time,
            )

        cvs.offset = self._offset # annotate offset for later use

        return cvs

    def __get__(self, obj, objtype = None):
        """
        Simulate func_descr_get() in Objects/funcobject.c
        https://stackoverflow.com/q/26226604/1672565
        """

        if obj is None:
            return self

        return MethodType(self, obj)

    @property
    def zindex_tag(self):

        return self._zindex_tag

    def register_effect(self, effect: EffectABC):

        self._effects.append(effect)

    def _to_pil(self, obj: Any) -> PIL_Image.Image:

        for canvas in inventory.values():
            if canvas.isinstance(obj, hard = False):
                return canvas.to_pil(obj)

        raise TypeError('unknown or unloaded canvas type coming from layer')
