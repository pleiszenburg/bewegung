# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/indexpool.py: Pools of unique index values

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

from typing import List

from .abc import IndexPoolABC
from .typeguard import typechecked

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class IndexPool(IndexPoolABC):
    """
    Used to manage z-index values and preparation taks between layers. index-values are unique.
    """

    def __init__(self):
        self._pool = set()

    def __repr__(self) -> str:
        return f'<IndexPool len={len(self):d}>'

    def __contains__(self, index: int) -> bool:
        return index in self._pool

    def __len__(self) -> int:
        return len(self._pool)

    @property
    def max(self) -> int:
        return max(self._pool)

    @property
    def min(self) -> int:
        return min(self._pool)

    def as_list(self) -> List[int]:
        return sorted(self._pool)

    def on_top(self) -> int:
        return (self.max + 1) if len(self) != 0 else 0

    def on_bottom(self) -> int:
        return (self.min - 1) if len(self) != 0 else 0

    def register(self, index: int):
        if index in self:
            raise IndexError()
        self._pool.add(index)
