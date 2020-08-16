# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/task.py: Render task

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

from typing import Callable, Union

from typeguard import typechecked

from .abc import CanvasTypes, SequenceABC, TaskABC, TimeABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Task(TaskABC):
    """
    Task for video renderer. Tasks can be ordered.
    """

    def __init__(self,
        sequence: SequenceABC,
        index: int,
        task: Callable[[TimeABC], CanvasTypes],
    ):

        self._sequence = sequence
        self._index = index
        self._task = task

    def __repr__(self):

        return f'<Task index={self._index:d}>'

    def __call__(self, time: TimeABC) -> Union[CanvasTypes, None]:

        return self._task(time)

    def __lt__(self, other: TaskABC):

        return self.index < other.index

    @property
    def index(self) -> int:

        return self._index

    @property
    def sequence(self) -> SequenceABC:

        return self._sequence
