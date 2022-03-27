# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/_array.py: Array base class

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

from abc import ABC, abstractmethod
from typing import Union

from ..lib import typechecked
from ._abc import (
    Iterable,
    MetaArrayDict,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class VectorArray(ABC, Iterable):
    """
    Abstract base class for all vector array types.

    Not intended to be instantiated.

    Args:
        meta : A dict holding arbitrary metadata
    """

    @abstractmethod
    def __init__(self, meta: Union[MetaArrayDict, None] = None):

        meta = {} if meta is None else dict(meta)

        if not all(value.ndim == 1 for value in meta.values()):
            raise ValueError('inconsistent: meta_value.ndim != 1')
        if not all(value.shape[0] == len(self) for value in meta.values()):
            raise ValueError('inconsistent length')

        self._meta = meta

    @property
    def meta(self) -> MetaArrayDict:
        """
        meta data dict
        """

        return self._meta
