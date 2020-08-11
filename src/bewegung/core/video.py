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

    def __init__(self, time: Time):

        self._time = time

        self._sequences = [] # list of sequences
        self._layers = [] # list of layers

    def sequence(self, start: Time, stop: Time) -> Callable:

        @typechecked
        def decorator(cls: type):

            @typechecked
            class wrapper(cls): # sequence class, setting time properties
                def __init__(other, *args, **kwargs):
                    other._start, other._stop = start, stop
                    super().__init__(*args, **kwargs)

            self._sequences.append(wrapper) # track sequence classes
            return None # wrapper # HACK remove original class?

        return decorator

    def layer(self, index: int) -> Callable:

        @typechecked
        def decorator(func: Callable):

            @typechecked
            def wrapper(other, time: Time):
                func.__globals__['time'] = time # inject time into namespace
                try:
                    ret = func(other)
                finally:
                    func.__globals__.pop('time') # cleanup namespace
                return ret

            wrapper.layer = index # tag wrapper function
            return wrapper

        return decorator

    def render(self):

        self._sequences[:] = [sequence() for sequence in self._sequences] # init sequences
        self._layers.extend([
            (getattr(sequence, attr).layer, getattr(sequence, attr))
            for sequence in self._sequences for attr in dir(sequence)
            if hasattr(getattr(sequence, attr), 'layer')
        ]) # find layer methods based on tags

        for frame in range(self._time):
            for idx, layer in self._layers:
                print( frame, idx, layer(frame) ) # call layer render functions
