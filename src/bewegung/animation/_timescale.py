# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_timescale.py: Time scaling

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

from datetime import datetime
from numbers import Number
from typing import Type

from ..lib import typechecked
from ._abc import TimeABC, TimeScaleABC
from ._time import Time

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: TimeScale
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class TimeScale(TimeScaleABC):
    """
    Convert between ``Time`` objects and custom integer & floating point time values.

    Immutable.

    Args:
        start : The time of start in the animation
        start_scaled : A number representing the begin of the the scaled time interval. Must have the same datatype as ``stop_scaled``.
        stop : The time of stop in the animation
        stop_scaled : A number representing the end of the the scaled time interval. Must have the same datatype as ``start_scaled``.
    """

    def __init__(self, start: TimeABC, start_scaled: Number, stop: TimeABC, stop_scaled: Number):

        if start.fps != stop.fps:
            raise ValueError()
        if type(start_scaled) != type(stop_scaled):
            raise TypeError('scaled start and stop times must be of equal type')

        self._start, self._stop, self._start_scaled, self._stop_scaled = start, stop, start_scaled, stop_scaled

        self._dtype = type(start_scaled)
        self._length, self._length_scaled = stop - start, self._stop_scaled - self._start_scaled
        self._scaled2time_factor = self._length.index / self._length_scaled
        self._time2scaled_factor = self._length_scaled / self._length.index

    def __repr__(self) -> str:

        if self._dtype == int:
            return (
                '<TimeScale '
                f'start_scaled={self._start_scaled:d} stop_scaled={self._stop_scaled:d} '
                f'start_index={self._start.index:d} stop_index={self._stop.index:d} fps={self.fps:d} '
                f'dtype={self._dtype.__name__:s}>'
            )

        return (
            '<TimeScale '
            f'start_scaled={self._start_scaled:e} stop_scaled={self._stop_scaled:e} '
            f'start_index={self._start.index:d} stop_index={self._stop.index:d} fps={self.fps:d} '
            f'dtype={self._dtype.__name__:s}>'
        )

    @property
    def dtype(self) -> Type:
        """
        Exposes dtype of object
        """

        return self._dtype

    @property
    def fps(self) -> int:
        """
        Frames per second
        """

        return self._start.fps

    @property
    def start(self) -> TimeABC:
        """
        Start animation time
        """

        return self._start

    @property
    def stop(self) -> TimeABC:
        """
        Stop animation time
        """

        return self._stop

    @property
    def start_scaled(self) -> Number:
        """
        Scaled start time
        """

        return self._start_scaled

    @property
    def stop_scaled(self) -> Number:
        """
        Scaled stop time
        """

        return self._stop_scaled

    def scaled2time(self, scaled_time: Number) -> TimeABC:
        """
        Converts scaled time to time in animation

        Args:
            scaled_time : A number representing scaled time
        """

        if not isinstance(scaled_time, self._dtype):
            raise TypeError('scaled time does not match dtype')

        rel_scaled_time = scaled_time - self._start_scaled
        index = round(rel_scaled_time * self._scaled2time_factor)

        return Time(fps = self._start.fps, index = self._start.index + index)

    def time2scaled(self, time: TimeABC) -> Number:
        """
        Converts time in animation to scaled time

        Args:
            time : Time in animation
        """

        rel_time = time - self._start
        scaled_time = rel_time.index * self._time2scaled_factor

        if self._dtype == int:
            scaled_time = round(scaled_time)

        return self._start_scaled + scaled_time

    @staticmethod
    def dt2msint(dt: datetime) -> int:
        """
        Converts a Python ``datetime.datetime`` object to milliseconds

        Args:
            dt : Date with (optionally) time and (optionally) time zone information attached
        """

        return int(dt.timestamp() * 1000)

    @staticmethod
    def iso2dt(isodate: str) -> datetime:
        """
        Converts a ISO-formatted date to a Python ``datetime.datetime`` object

        Args:
            isodate : A date (and time) following the ISO date format
        """

        return datetime.fromisoformat(isodate)
