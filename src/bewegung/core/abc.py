# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/abc.py: Abstract base classes

    Copyright (C) 2020-2021 Sebastian M. Ernst <ernst@pleiszenburg.de>

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

from abc import ABC
from typing import Tuple, Union

try:
    import numpy as np
except ModuleNotFoundError:
    np = None

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class BackendABC(ABC):
    pass

class ColorABC(ABC):
    pass

class EffectABC(ABC):
    pass

class EncoderABC(ABC):
    pass

class IndexPoolABC(ABC):
    pass

class LayerABC(ABC):
    pass

class SequenceABC(ABC):
    pass

class TaskABC(ABC):
    pass

class TimeABC(ABC):
    pass

class TimeScaleABC(ABC):
    pass

class VideoABC(ABC):
    pass

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Types
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

PyNumber = Union[int, float]
PyNumber2D = Union[Tuple[int, int], Tuple[float, float]]
PyNumber3D = Union[Tuple[int, int, int], Tuple[float, float, float]]

if np is not None:
    Dtype = Union[str, np.dtype]
else:
    Dtype = None # HACK
