# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_effects.py: Video frame effects

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

import math

from PIL import Image as PIL_Image

from ..lib import typechecked
from ._abc import EffectABC, LayerABC, SequenceABC, TimeABC, VideoABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: BASE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class EffectBase(EffectABC):
    """
    Base for all effect classes - not an effect on its own. Derive new effect classes from this class.
    Decorator for layers.

    Mutable.

    If the orginal cunstructor method is overridden, it must be called from the child class.
    """

    def __init__(self):

        apply = getattr(self.apply, '__wrapped__', self.apply) # typeguard
        self._args = apply.__code__.co_varnames[
            1:apply.__code__.co_argcount # excluding self and internal namespace
            ] # parameters requested by user
        assert self._args[0] == 'cvs' # canvas

    def __repr__(self) -> str:

        return f'<{type(self).__name__}>'

    def __call__(self, layer: LayerABC) -> LayerABC:
        """
        Decorator function, decorating :class:`bewegung.core.layer.Layer` objects (wrapping user-defined layer methods).
        The effect is registered via :meth:`bewegung.core.layer.Layer.register_effect` and returns the otherwise unchanged layer object.

        Do not override!

        Args:
            layer : Layer to which the effect is applied.
        """

        layer.register_effect(self)
        return layer

    def apply_(self,
        cvs: PIL_Image.Image,
        video: VideoABC,
        sequence: SequenceABC,
        time: TimeABC,
        ) -> PIL_Image.Image:
        """
        Internal interface for layer objects. Applies the effect to a Pillow Image object and returns the modified image.
        The function automatically determines what arguments the ``apply`` method of an actual effect requests other than ``cvs``.
        Possible options are:

        - video: Parent video object
        - sequence: Parent sequence object
        - time: Time within parent video
        - reltime: Relative time within parent sequence

        Do not override!

        Args:
            cvs : Input Pillow Image object
            video : Parent video object
            sequence : Parent sequence object
            time : Time within parent video
        """

        kwargs = {}
        for arg in self._args[1:]:
            if arg == 'video':
                kwargs['video'] = video
            elif arg == 'sequence':
                kwargs['sequence'] = sequence
            elif arg == 'time':
                kwargs['time'] = time
            elif arg == 'reltime':
                kwargs['reltime'] = time - sequence.start
            else:
                raise ValueError('unknown argument')

        return self.apply(cvs = cvs, **kwargs)

    def apply(self, cvs: PIL_Image.Image):
        """
        Applies effect to image.

        Must be reimplemented!

        Args:
            cvs : Input Pillow Image object
        """

        raise NotImplementedError()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES: EFFECTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class FadeInEffect(EffectBase):
    """
    Fade-in effect. Decorator for layers.

    Args:
        blend_time : Duration of effect relative to the beginning of the parent sequence
    """

    def __init__(self, blend_time: TimeABC):

        if blend_time.index < 0:
            raise ValueError('time must be positive or zero')

        super().__init__()
        self._blend_time = blend_time

    def apply(self, cvs: PIL_Image.Image, sequence: SequenceABC, time: TimeABC,) -> PIL_Image.Image:

        reltime = time - sequence.start
        if reltime > self._blend_time:
            return cvs

        r, g, b, a = cvs.split()
        factor = _sin_fade(reltime.index / self._blend_time.index)
        a = a.point(lambda i: i * factor)

        return PIL_Image.merge('RGBA', (r, g, b, a))

@typechecked
class FadeOutEffect(EffectBase):
    """
    Fade-out effect. Decorator for layers.

    Args:
        blend_time : Duration of effect relative to the beginning of the parent sequence
    """

    def __init__(self, blend_time: TimeABC):

        if blend_time.index < 0:
            raise ValueError('time must be positive or zero')

        super().__init__()
        self._blend_time = blend_time

    def apply(self, cvs: PIL_Image.Image, sequence: SequenceABC, time: TimeABC,) -> PIL_Image.Image:

        if time < sequence.stop - self._blend_time:
            return cvs
        nreltime = sequence.stop - time

        r, g, b, a = cvs.split()
        factor = _sin_fade(nreltime.index / self._blend_time.index)
        a = a.point(lambda i: i * factor)

        return PIL_Image.merge('RGBA', (r, g, b, a))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES: HELPER
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def _sin_fade(factor: float) -> float:

    assert 0.0 <= factor <= 1.0

    return -math.cos(factor * math.pi) / 2 + 0.5
