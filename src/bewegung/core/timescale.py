# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/timescale.py: Time scaling

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

from datetime import datetime

from typeguard import typechecked

from .abc import TimeScaleABC
from .time import Time

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: TimeScale
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class TimeScale(TimeScaleABC):
    """
    Convert between Time objects and custom integer time values.
    """

    def __init__(self, start: Time, start_scaled: int, stop: Time, stop_scaled: int):
        if start.fps != stop.fps:
            raise ValueError()
        self._start, self._stop, self._start_scaled, self._stop_scaled = start, stop, start_scaled, stop_scaled
        self._length, self._length_scaled = stop - start, self._stop_scaled - self._start_scaled
        self._scaled2time_factor = self._length.index / self._length_scaled
        self._time2scaled_factor = self._length_scaled / self._length.index

    def scaled2time(self, scaled_time: int) -> Time:
        rel_scaled_time = scaled_time - self._start_scaled
        index = round(rel_scaled_time * self._scaled2time_factor)
        return Time(fps = self._start.fps, index = self._start.index + index)

    def time2scaled(self, time: Time) -> int:
        rel_time = time - self._start
        scaled_index = round(rel_time.index * self._time2scaled_factor)
        return self._start_scaled + scaled_index

    @staticmethod
    def dt2msint(dt: datetime) -> int:
        return int(dt.timestamp() * 1000)

    @staticmethod
    def iso2dt(isodate: str) -> datetime:
        return datetime.fromisoformat(isodate)
