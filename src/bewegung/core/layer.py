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
from typing import Callable, Tuple, Union

from cairo import ImageSurface, Format
from datashader.transfer_functions import Image as DS_Image
from PIL import Image as PIL_Image, ImageOps as PIL_ImageOps
from typeguard import typechecked

from .abc import CanvasTypes, DrawingBoardABC, EffectABC, LayerABC, SequenceABC, TimeABC, VideoABC
from .drawingboard import DrawingBoard

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
        canvas: Union[Callable[[], CanvasTypes], None] = None,
        box: Tuple[int, int] = (0, 0),
    ):

        self._method = method
        self._zindex_tag = zindex
        self._video = video
        self._canvas = self._video.db_canvas() if canvas is None else canvas
        self._box = box
        self._effects = []

        self._args = self._method.__code__.co_varnames[
            1:self._method.__code__.co_argcount # excluding self and internal namespace
            ] # parameters requested by user

    def __repr__(self) -> str:

        return f'<Layer name={self._method.__name__:s} zindex={self._zindex_tag:d}>'

    def __call__(self, sequence: SequenceABC, time: TimeABC) -> PIL_Image.Image:

        kwargs = {}
        for param in self._args:
            if param == 'time':
                kwargs[param] = time
            elif param == 'reltime':
                kwargs[param] = time - sequence.start
            elif param == 'canvas':
                kwargs[param] = self._canvas()
            else:
                raise ValueError('unknown parameter')

        cvs = self._method(sequence, **kwargs)

        if isinstance(cvs, PIL_Image.Image):
            assert cvs.mode == 'RGBA'
        elif isinstance(cvs, DS_Image):
            cvs = cvs.to_pil()
            assert cvs.mode == 'RGBA'
            cvs = PIL_ImageOps.flip(cvs) # datashader's y axis must be flipped
        elif isinstance(cvs, DrawingBoardABC):
            cvs = cvs.as_pil()
        elif isinstance(cvs, ImageSurface):
            assert cvs.get_format() == Format.ARGB32
            cvs = DrawingBoard.swap_channels(PIL_Image.frombuffer(
                mode = 'RGBA',
                size = (cvs.get_width(), cvs.get_height()),
                data = cvs.get_data(),
                ))
        else:
            raise TypeError('unknown canvas type coming from layer')

        for effect in self._effects:
            cvs = effect.apply_(
                cvs = cvs,
                video = self._video,
                sequence = sequence,
                time = time,
            )

        cvs.box = self._box # annotate offset for later use

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
