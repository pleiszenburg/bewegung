# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_time.py: Time handling

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

from typing import Generator, Union

from ..lib import typechecked
from ._abc import TimeABC
from ._const import FPS_DEFAULT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Time(TimeABC):
    """
    This class represents time both as number of frames (the index) and time in seconds.
    For conversion, it has an internal frames per second state.
    Operators for basic arithmetic such as add and substract are implemented.
    Comparison operators are implemented.
    Operations can only be performed on ``Time`` objects with equal frames per second.
    If frames per second are unequal, an exception will be raised.

    Immutable.

    Args:
        fps : Frames per second
        index : Number of frames
    """

    def __init__(self, fps: int = FPS_DEFAULT, index: int = 0):

        if fps <= 0:
            raise ValueError('there must be at least one frame per second')

        self._fps, self._index = fps, index

    def __repr__(self) -> str:

        return f'<Time index={self._index:d} seconds={self.seconds:.03f}s fps={self._fps:d}>'

    def __int__(self) -> int:
        """
        If converted to an integer, the frame number (index) will be exposed.
        """

        return self._index

    def __float__(self) -> float:
        """
        If converted to a floating point number, the time in seconds will be exposed.
        """

        return self.seconds

    def __eq__(self, other: TimeABC) -> bool:
        self._assert_fps(other)
        return self.index == other.index

    def __lt__(self, other: TimeABC) -> bool:
        self._assert_fps(other)
        return self.index < other.index

    def __le__(self, other: TimeABC) -> bool:
        self._assert_fps(other)
        return self.index <= other.index

    def __gt__(self, other: TimeABC) -> bool:
        self._assert_fps(other)
        return self.index > other.index

    def __ge__(self, other: TimeABC) -> bool:
        self._assert_fps(other)
        return self.index >= other.index

    def __add__(self, other: TimeABC) -> TimeABC:
        self._assert_fps(other)
        return type(self)(self.fps, self.index + other.index)

    def __sub__(self, other: TimeABC) -> TimeABC:
        self._assert_fps(other)
        return type(self)(self.fps, self.index - other.index)

    def __truediv__(self, other: TimeABC) -> float:
        self._assert_fps(other)
        return self.index / other.index

    def _assert_fps(self, other):
        if self.fps != other.fps:
            raise ValueError()

    @property
    def fps(self) -> int:
        """
        Frames per second
        """

        return self._fps

    @property
    def index(self) -> int:
        """
        Time as number of frames
        """

        return self._index

    @property
    def seconds(self) -> float:
        """
        Time in seconds
        """

        return self._index / self._fps # float

    def time(self, index: int) -> TimeABC:
        """
        Generates a new ``Time`` object from a given number of frames based on the time's frames per second.

        Args:
            index : Number of frames
        """

        return type(self)(fps = self._fps, index = index)

    def time_from_seconds(self, seconds: Union[float, int]) -> TimeABC:
        """
        Generates a new ``Time`` object from a given time in seconds based on the time's frames per second.

        Args:
            seconds : Time in seconds
        """

        return type(self).from_seconds(fps = self._fps, seconds = seconds)

    @classmethod
    def from_seconds(cls, fps: int = FPS_DEFAULT, seconds: Union[float, int] = 1.0) -> TimeABC:
        """
        Constructs a new ``Time`` object from frames per second and seconds.

        Args:
            fps : Frames per second
            seconds : Time in seconds
        """

        if isinstance(seconds, int):
            seconds = float(seconds)

        return cls(fps = fps, index = round(seconds * fps))

    @classmethod
    def range(cls, start: TimeABC, stop: TimeABC) -> Generator[TimeABC, None, None]:
        """
        Generator function, similar to Python's range. Generates Time objects instead, frame by frame.

        Args:
            start : Start time of range. ``start.fps`` must be equal to ``stop.fps``.
            stop : Stop time of range (not included). ``start.fps`` must be equal to ``stop.fps``.
        """

        if start.fps != stop.fps:
            raise ValueError()
        if start.index >= stop.index:
            raise ValueError()
        for index in range(start.index, stop.index):
            yield cls(fps = start.fps, index = index)
