# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_layer.py: Layer function/method wrapper

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

from types import MethodType
from typing import Any, Callable, Union

from PIL import Image as PIL_Image

from ..lib import typechecked
from ..linalg import Vector2D
from ._abc import EffectABC, LayerABC, SequenceABC, TimeABC, VideoABC
from ._backends import backends

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Layer(LayerABC):
    """
    Callable layer method wrapper (decorator), managing rendering and application of effects.
    Do not instantiate this class or derive from it - use the :meth:`bewegung.Video.layer` decorator instead!

    Mutable.

    Args:
        method : Wrapped layer method from a user-defined sequence class
        zindex : A number, managed by an :class:`bewegung.IndexPool` object (:attr:`bewegung.Video.zindex`),
            representing the relative position within a stack of ``layer`` tasks.
        video : Parent video object
        canvas : A function pointer to a factory function, generating a new canvas once per frame for the ``layer`` task.
            The pointer is typically generated by the :meth:`bewegung.Video.canvas` method.
        offset : The layer's offset relative to the top-left corner of the video. The y-axis is downwards positive.
    """

    def __init__(self,
        method: Callable,
        zindex: int,
        video: VideoABC,
        canvas: Union[Callable, None] = None,
        offset: Union[Vector2D, None] = None,
    ):

        # consistency checks are performed in Video.layer

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
        """
        Wraps layer method from a user-defined sequence class.
        This method determines what parameters the user-defined layer method requested.
        Possible options are:

        - ``time``: The absolute time within the parent video
        - ``reltime``: The relative time within the parent sequence
        - ``canvas``: An empty canvas

        Subsequently, the user-defined layer method is called with the requested parameters.
        It then converts the returned canvas to a Pillow Image object
        by making the currently loaded backends recognize the returned canvas type.
        Finally, effects are applied and the Pillow Image object is returned.

        Args:
            sequence : Parent sequence
            time : Time within video
        """

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
        # Simulate ``func_descr_get()`` in ``Objects/funcobject.c``, see `stackoverflow`_.
        # .. _stackoverflow: https://stackoverflow.com/q/26226604/1672565

        if obj is None:
            return self

        return MethodType(self, obj)

    @property
    def zindex_tag(self) -> int:
        """
        z-index of layer
        """

        return self._zindex_tag

    def register_effect(self, effect: EffectABC):
        """
        Interface used by effects decorators to register themselves. See :meth:`bewegung.EffectBase.__call__`.

        Args:
            effect : Configured effect object
        """

        self._effects.append(effect)

    def _to_pil(self, obj: Any) -> PIL_Image.Image:
        """
        Detects the datatype of the canvas returned by the user-defined layer method and tries to convert it to a Pillow Image.
        Raises a type error if none of the currently loaded backends recognizes the canvas type.

        Args:
            obj : A canvas object
        """

        for backend in backends.values():
            if backend.isinstance(obj, hard = False):
                return backend.to_pil(obj)

        raise TypeError('unknown or unloaded backend canvas type coming from layer')
