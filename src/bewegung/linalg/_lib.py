# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/_lib.py: Linear algebra library

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

from ..lib import typechecked
from ._abc import Dtype, NumberType
from ._numpy import np

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def dtype_np2py(dtype: Dtype) -> NumberType:
    """
    Map numpy dtypes to Python number types
    """

    if np.issubdtype(dtype, np.integer):
        return int
    elif np.issubdtype(dtype, np.floating):
        return float
    else:
        raise TypeError("numpy dtype can not be mapped on Python number types")

@typechecked
def dtype_name(dtype: Dtype) -> str:
    """
    Provides name of both Python and numpy number/array types
    """

    return getattr(
        dtype, '__name__',
        str(dtype), # fallback, numpy
    )
