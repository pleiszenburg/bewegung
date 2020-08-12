# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/video.py: Parallel video frame renderer

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

from typing import Callable

from typeguard import typechecked

from .indexpool import IndexPool
from .time import Time

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# "GLOBALS" (FOR WORKERS)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# _context = {}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Video:
    """
    Mutable. Decorators ...
    """

    def __init__(self, time: Time, width: int, height: int):

        assert time.index > 0
        assert width > 0
        assert height > 0

        self._time = time
        self._width = width
        self._height = height

        self._sequences = [] # list of sequences

        self._layers = [] # list of layers
        self._zindex = IndexPool()

    @property
    def time(self) -> Time:
        return self._time

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def zindex(self) -> IndexPool:
        return self._zindex

    def sequence(self, start: Time, stop: Time) -> Callable:

        @typechecked
        def decorator(cls: type):

            @typechecked
            class wrapper(cls): # sequence class, setting time properties
                def __init__(other, *args, **kwargs):
                    other._start, other._stop = start, stop
                    super().__init__(*args, **kwargs)
                def __contains__(other, time: Time) -> bool:
                    return other._start <= time and time < other._stop
                @property
                def start(other) -> Time:
                    return self._start
                @property
                def stop(other) -> Time:
                    return self._stop

            self._sequences.append(wrapper) # track sequence classes
            return None # wrapper # HACK remove original class?

        return decorator

    def layer(self, zindex: int) -> Callable:

        self._zindex.register(zindex) # ensure unique z-index

        @typechecked
        def decorator(func: Callable):

            @typechecked
            def wrapper(other, time: Time): # TODO add canvas type & size param
                func.__globals__['time'] = time # inject time into namespace
                # TODO inject newly created canvas and relative time?
                try:
                    ret = func(other)
                finally:
                    func.__globals__.pop('time') # cleanup namespace
                # TODO convert whatever image type "ret" has to PIL
                return ret

            wrapper.layer = zindex # tag wrapper function
            return wrapper

        return decorator

    # TODO prepare - similar to "layer"
    # TODO "after effects" - similar to "layer"

    def render(self, parallel: bool = False):

        self._sequences[:] = [sequence() for sequence in self._sequences] # init sequences
        # TODO re-init classes for next renderer run?

        self._layers.clear()
        self._layers.extend([
            (sequence, getattr(sequence, attr).layer, getattr(sequence, attr))
            for sequence in self._sequences for attr in dir(sequence)
            if hasattr(getattr(sequence, attr), 'layer')
        ]) # find layer methods based on tags
        self._layers.sort(key = lambda x: x[1]) # sort by z-index

        # TODO branch for parallel frame rendering

        for time in Time.range(Time(fps = self._time.fps, index = 0), self._time):
            frame = self.render_frame(time)

        # TODO optionally write frames to files
        # TODO optionally pipe frames to ffmpeg

    def render_frame(self, time):

        layers = [
            layer(time)
            for sequence, _, layer in self._layers
            if time in sequence
        ] # call layer render functions

        # TODO merge layers

        return None # TODO composit image
