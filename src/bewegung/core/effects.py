# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/effects.py: Video frame effects

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

import math

from PIL import Image as PIL_Image

from .abc import EffectABC, LayerABC, SequenceABC, TimeABC, VideoABC
from .typeguard import typechecked

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: BASE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class BaseEffect(EffectABC):
    """
    Mutable. Base for all effect classes - not effect on its own.
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
        Decorator function.
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
        Internal interface for layer. Do not re-implement.
        """

        kwargs = {}
        for arg in self._args[1:]:
            if arg == 'video':
                kwargs['video'] = video
            elif arg == 'sequence':
                kwargs['sequence'] = sequence
            elif arg == 'time':
                kwargs['time'] = time
            else:
                raise ValueError('unknown argument')

        return self.apply(cvs = cvs, **kwargs)

    def apply(self, cvs: PIL_Image.Image):
        """
        Re-implement this for effects.
        """

        raise NotImplementedError()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES: EFFECTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class FadeInEffect(BaseEffect):

    def __init__(self, blend_time: TimeABC):

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
class FadeOutEffect(BaseEffect):

    def __init__(self, blend_time: TimeABC):

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
