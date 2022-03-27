# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_indexpool.py: Pools of unique index values

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

from typing import List

from ..lib import typechecked
from ._abc import IndexPoolABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class IndexPool(IndexPoolABC):
    """
    Used to manage z-index for layers tasks and prepare-order ("preporder") values ("indices") for prepare tasks.
    Indices, represented by integers, are unique within a pool.
    New pools are empty.

    Mutable.
    """

    def __init__(self):

        self._pool = set()

    def __repr__(self) -> str:

        return f'<IndexPool len={len(self):d}>'

    def __contains__(self, index: int) -> bool:
        """
        Checks whether an index is already present in the pool.

        Args:
            index : Value that should be checked
        """

        return index in self._pool

    def __len__(self) -> int:
        """
        Number of entries in the pool
        """

        return len(self._pool)

    @property
    def max(self) -> int:
        """
        Highest index currently present in pool
        """

        return max(self._pool)

    @property
    def min(self) -> int:
        """
        Lowest index currently present in pool
        """

        return min(self._pool)

    def as_list(self) -> List[int]:
        """
        Exports pool as a sorted list
        """

        return sorted(self._pool)

    def on_top(self) -> int:
        """
        Returns an index that would be on top of the pool, i.e. ``max + 1``. If the pool is empty, it returns 0.
        The index is not automatically added (registered) to the pool.
        """

        return (self.max + 1) if len(self) != 0 else 0

    def on_bottom(self) -> int:
        """
        Returns an index that would be on the bottom of the pool, i.e. ``min - 1``. If the pool is empty, it returns 0.
        The index is not automatically added (registered) to the pool.
        """

        return (self.min - 1) if len(self) != 0 else 0

    def register(self, index: int):
        """
        Registers, i.e. adds an index to the pool. Raises an exception if the index is already present in the pool.

        Args:
            index : Value that should be added to the pool
        """

        if index in self:
            raise IndexError('index is already present in pool')

        self._pool.add(index)
