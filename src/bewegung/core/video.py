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

from typing import Callable, Dict, Union

from cairo import FORMAT_ARGB32, ImageSurface
from datashader import Canvas
from PIL import Image
from typeguard import typechecked

from .abc import SequenceABC
from .drawingboard import DrawingBoard
from .indexpool import IndexPool
from .task import Task
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

    def __init__(self,
        time: Time, # video length and frame rate
        width: int, # video width
        height: int, # video height
        ctx: Union[Dict, None] = None, # store for video context data
    ):

        assert time.index > 0
        assert width > 0
        assert height > 0

        self._time = time
        self._width = width
        self._height = height
        self._ctx = ctx if ctx is not None else {}

        self._sequences = [] # list of sequences

        self._layertasks = [] # list of layer render tasks
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
    def ctx(self) -> Dict:
        return self._ctx

    @property
    def zindex(self) -> IndexPool:
        return self._zindex

    def sequence(self,
        start: Union[Time, None] = None,
        stop: Union[Time, None] = None,
    ) -> Callable:

        if start is None:
            start = Time(fps = self._time.fps, index = 0)
        if stop is None:
            stop = self._time

        if start.fps != self._time.fps:
            start = Time.from_time(fps = self._time.fps, time = start.time)
        if stop.fps != self._time.fps:
            stop = Time.from_time(fps = self._time.fps, time = stop.time)

        if start < Time(fps = self._time.fps, index = 0):
            raise ValueError()
        if stop > self._time:
            raise ValueError()
        if start >= stop:
            raise ValueError()

        @typechecked
        def decorator(cls: type):

            @typechecked
            class wrapper(cls, SequenceABC): # sequence class, setting time properties
                def __init__(other, *args, **kwargs):
                    other._start, other._stop = start, stop
                    super().__init__(*args, **kwargs) # TODO super/cls?
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

    def cairo_layer(self, **kwargs):

        if 'format' not in kwargs.keys():
            kwargs['format'] = FORMAT_ARGB32
        if 'width' not in kwargs.keys():
            kwargs['width'] = self._width
        if 'height' not in kwargs.keys():
            kwargs['height'] = self._height

        return lambda: ImageSurface(kwargs['format'], kwargs['width'], kwargs['height'])

    def db_layer(self, **kwargs):

        if 'width' not in kwargs.keys():
            kwargs['width'] = self._width
        if 'height' not in kwargs.keys():
            kwargs['height'] = self._height

        return lambda: DrawingBoard(**kwargs)

    def ds_layer(self, **kwargs):

        if 'plot_width' not in kwargs.keys():
            kwargs['plot_width'] = self._width
        if 'plot_height' not in kwargs.keys():
            kwargs['plot_height'] = self._height

        if 'x_range' not in kwargs.keys():
            kwargs['x_range'] = (0, self._width)
        if 'y_range' not in kwargs.keys():
            kwargs['y_range'] = (0, self._height)

        return lambda: Canvas(**kwargs)

    def pil_layer(self, **kwargs):

        if 'mode' not in kwargs.keys():
            kwargs['mode'] = 'RGBA'
        if 'size' not in kwargs.keys():
            kwargs['size'] = (self._width, self._height)

        return lambda: Image(**kwargs)

    def layer(self,
        zindex: int, # TODO add canvas type & size param, offset param
    ) -> Callable:

        self._zindex.register(zindex) # ensure unique z-index

        # Canvas:
        # - DrawingBoard
        # - Raw PIL
        # - Raw Cairo surface
        # - Datashader
        # - QGIS / Matplotlib / ... ?

        @typechecked
        def decorator(func: Callable):

            @typechecked
            def wrapper(other, sequence: SequenceABC, time: Time):

                # TODO inject newly created canvas and relative time

                ret = func(other,
                    time = time,
                    reltime = time - sequence.start,
                )

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

        self._layertasks.clear()
        self._layertasks.extend([
            Task(
                sequence = sequence,
                index = getattr(sequence, attr).layer,
                task = getattr(sequence, attr),
            )
            for sequence in self._sequences for attr in dir(sequence)
            if hasattr(getattr(sequence, attr), 'layer')
        ]) # find layer methods based on tags
        self._layertasks.sort() # sort by (z-) index

        # TODO branch for parallel frame rendering

        for time in Time.range(Time(fps = self._time.fps, index = 0), self._time):
            frame = self.render_frame(time)

        # TODO optionally write frames to files
        # TODO optionally pipe frames to ffmpeg

    def render_frame(self, time: Time):

        layers = [
            layertask(time)
            for layertask in self._layertasks
            if time in layertask.sequence
        ] # call layer render functions

        # TODO merge layers

        return None # TODO composit image
