# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/time.py: Time handling

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

from typing import Generator, Union

from typeguard import typechecked

from .abc import TimeABC
from .const import FPS_DEFAULT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Time(TimeABC):
    """
    Immutable.
    """

    def __init__(self, fps: int = FPS_DEFAULT, index: int = 0):
        if fps <= 0:
            raise ValueError()
        self._fps, self._index = fps, index

    def __repr__(self):
        return f'<Time index={self._index:d} seconds={self.seconds:.03f}s fps={self._fps:d}>'

    def __eq__(self, other: TimeABC):
        self._assert_fps(other)
        return self.index == other.index

    def __lt__(self, other: TimeABC):
        self._assert_fps(other)
        return self.index < other.index

    def __le__(self, other: TimeABC):
        self._assert_fps(other)
        return self.index <= other.index

    def __gt__(self, other: TimeABC):
        self._assert_fps(other)
        return self.index > other.index

    def __ge__(self, other: TimeABC):
        self._assert_fps(other)
        return self.index >= other.index

    def __add__(self, other: TimeABC):
        self._assert_fps(other)
        return type(self)(self.fps, self.index + other.index)

    def __sub__(self, other: TimeABC):
        self._assert_fps(other)
        return type(self)(self.fps, self.index - other.index)

    def _assert_fps(self, other):
        if self.fps != other.fps:
            raise ValueError()

    @property
    def fps(self):
        return self._fps

    @property
    def index(self):
        return self._index

    @property
    def seconds(self):
        return self._index / self._fps # float

    def time(self, index: int) -> TimeABC:

        return type(self)(fps = self._fps, index = index)

    def time_from_seconds(self, seconds: Union[float, int]) -> TimeABC:

        return type(self).from_seconds(fps = self._fps, seconds = seconds)

    @classmethod
    def from_seconds(cls, fps: int = FPS_DEFAULT, seconds: Union[float, int] = 1.0):
        if isinstance(seconds, int):
            seconds = float(seconds)
        return cls(fps = fps, index = round(seconds * fps))

    @classmethod
    def range(cls, start: TimeABC, stop: TimeABC) -> Generator[TimeABC, None, None]:
        if start.fps != stop.fps:
            raise ValueError()
        if start.index >= stop.index:
            raise ValueError()
        for index in range(start.index, stop.index):
            yield cls(fps = start.fps, index = index)
