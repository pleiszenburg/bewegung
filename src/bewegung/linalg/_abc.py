# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/_abc.py: Abstract base classes

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

from abc import ABC
from numbers import Number
import sys
from typing import Dict, Tuple, Type, TypeVar, Union

from ._numpy import np, ndarray

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class CameraABC(ABC):
    pass

class MatrixABC(ABC):
    pass

class MatrixArrayABC(ABC):
    pass

class VectorArray2DABC(ABC):
    pass

class VectorArray3DABC(ABC):
    pass

class Vector2DABC(ABC):
    pass

class Vector3DABC(ABC):
    pass

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Types
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

NumberType = Type[Number]

if np is not None:
    Dtype = Union[str, NumberType, np.dtype]
else:
    Dtype = None # HACK

Numbers = TypeVar('N', bound = Number)
Number2D = Tuple[Numbers, Numbers]
Number3D = Tuple[Numbers, Numbers, Numbers]

try:
    from typing import NotImplementedType # re-introduced in Python 3.10
except ImportError:
    NotImplementedType = type(NotImplemented)

MetaDict = Dict[str, Union[str, bytes, Number]]
MetaArrayDict = Dict[str, ndarray]

assert sys.version_info.major == 3
if sys.version_info.minor > 8:
    from collections.abc import Iterable
else:
    from typing import Iterable
