# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/abc.py: Abstract base classes

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
from typing import Generator, List, Tuple, Union

try:
    import numpy as np
except ModuleNotFoundError:
    np = None

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class CameraABC(ABC):
    pass

class MatrixABC(ABC):
    pass

class MatrixArrayABC(ABC):
    pass

class VectorABC(ABC):
    pass

class VectorArrayABC(ABC):
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

VectorIterable2D = Union[
    List[Vector2DABC],
    Tuple[Vector2DABC],
    Generator[Vector2DABC, None, None],
]

VectorIterable3D = Union[
    List[Vector3DABC],
    Tuple[Vector3DABC],
    Generator[Vector3DABC, None, None],
]

if np is not None:
    Dtype = Union[str, np.dtype]
else:
    Dtype = None # HACK
