# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/__init__.py: Package root

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
# EXPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

__version__ = '0.0.1'

from .core.camera import Camera
from .core.backends import *
from .core.color import Color
from .core.const import *
from .core.effects import EffectBase, FadeInEffect, FadeOutEffect
from .core.encoders import EncoderBase, FFmpegH264Encoder, FFmpegGifEncoder
from .core.indexpool import IndexPool
from .core.layer import Layer
from .core.sequence import Sequence
from .core.task import Task
from .core.time import Time
from .core.timescale import TimeScale
from .core.vector import *
from .core.video import Video
