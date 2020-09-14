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

import inspect
import multiprocessing as mp
from subprocess import Popen, PIPE, DEVNULL
from typing import Callable, Dict, Union, Tuple

from PIL import Image as PIL_Image
from tqdm import tqdm
from typeguard import typechecked

from .abc import LayerABC, SequenceABC, VideoABC
from .canvas import inventory
from .const import FPS_DEFAULT
from .indexpool import IndexPool
from .layer import Layer
from .sequence import Sequence
from .task import Task
from .time import Time

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# "GLOBALS" (FOR WORKERS)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

_workers = {}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Video(VideoABC):
    """
    Mutable. Decorators ...
    """

    def __init__(self,
        width: int, # video width
        height: int, # video height
        ctx: Union[Dict, None] = None, # store for video context data
        fps: int = FPS_DEFAULT,
        seconds: Union[float, int, None] = None,
        frames: Union[int, None] = None,
    ):

        assert width > 0
        assert height > 0

        self._width = width
        self._height = height
        self._ctx = ctx if ctx is not None else {}

        assert fps > 0
        assert (seconds is not None) ^ (frames is not None)
        if seconds is not None:
            assert seconds > 0
        if frames is not None:
            assert frames > 0
        self._length = Time(
            fps = fps, index = frames,
            ) if seconds is None else Time.from_seconds(
            fps = fps, seconds = seconds,
        )

        self._sequences = [] # list of sequences

        self._preptasks = [] # list of sequence prepare tasks
        self._layertasks = [] # list of layer render tasks
        self._preporder = IndexPool()
        self._zindex = IndexPool()

    def __repr__(self) -> str:

        return f'<Video frames={self._length.index:d} seconds={self._length.seconds:.03f}s fps={self.fps:d}>'

    def __len__(self) -> int:

        return self._length.index

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PROPERTIES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @property
    def length(self) -> Time:
        return self._length

    @property
    def fps(self) -> int:
        return self._length.fps

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
    def preporder(self) -> IndexPool:
        return self._preporder

    @property
    def zindex(self) -> IndexPool:
        return self._zindex

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# RESET TASKS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def time(self, index: int) -> Time:

        return self._length.time(index = index)

    def time_from_seconds(self, seconds: Union[float, int]) -> Time:

        return self._length.time_from_seconds(seconds = seconds)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# RESET TASKS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def reset(self):

        for sequence in self._sequences:
            sequence.reset()

        self._preptasks.clear()
        self._preptasks.extend([
            Task(
                sequence = sequence,
                index = getattr(sequence, attr).preporder_tag,
                task = getattr(sequence, attr),
            )
            for sequence in self._sequences for attr in dir(sequence)
            if hasattr(getattr(sequence, attr), 'preporder_tag')
        ]) # find prepare methods based on tags
        self._preptasks.sort() # sort by preporder

        self._layertasks.clear()
        self._layertasks.extend([
            Task(
                sequence = sequence,
                index = getattr(sequence, attr).zindex_tag,
                task = getattr(sequence, attr),
            )
            for sequence in self._sequences for attr in dir(sequence)
            if hasattr(getattr(sequence, attr), 'zindex_tag')
        ]) # find layer methods based on tags
        self._layertasks.sort() # sort by (z-) index

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# DECORATOR: SEQUENCE (TYPE)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def sequence(self,
        start: Union[Time, None] = None,
        stop: Union[Time, None] = None,
    ) -> Callable:

        if start is None:
            start = self.time(0)
        if stop is None:
            stop = self._length

        if start.fps != self.fps:
            start = self.time_from_seconds(seconds = start.seconds)
        if stop.fps != self.fps:
            stop = self.time_from_seconds(seconds = stop.seconds)

        if start < self.time(0):
            start = self._length + start
        if not (self.time(0) <= start <= self._length):
            raise ValueError()
        if stop < self.time(0):
            stop = self._length + stop
        if not (self.time(0) <= stop <= self._length):
            raise ValueError()

        if start >= stop:
            raise ValueError()

        @typechecked
        def decorator(cls: type):

            cls_bases, sequence_bases = inspect.getmro(cls), inspect.getmro(Sequence)
            bases = tuple([item for item in sequence_bases if item not in cls_bases]) + cls_bases
            SequenceCls = type(cls.__name__, bases, Sequence.__dict__.copy())
            sequence = SequenceCls(start = start, stop = stop, video = self)

            self._sequences.append(sequence)
            return sequence # HACK return object, not class

        return decorator

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# DECORATOR: PREPARE (TASK)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def prepare(self,
        preporder: int,
    ) -> Callable:

        self._preporder.register(preporder) # ensure unique preporder

        @typechecked
        def decorator(method: Callable) -> Callable:

            @typechecked
            def wrapper(sequence: SequenceABC, time: Time):

                kwargs = {}
                for param in method.__code__.co_varnames[
                    1:method.__code__.co_argcount # excluding self and internal namespace
                ]: # parameters requested by user
                    if param == 'time':
                        kwargs[param] = time
                    elif param == 'reltime':
                        kwargs[param] = time - sequence.start
                    else:
                        raise ValueError('unknown parameter', param)

                method(sequence, **kwargs) # let user draw layer/canvas for frame

            wrapper.preporder_tag = preporder # tag wrapper function
            return wrapper

        return decorator

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# DECORATOR: LAYER (TASK)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def layer(self,
        zindex: int,
        canvas: Union[Callable, None] = None,
        offset: Tuple[int, int] = (0, 0),
    ) -> Callable:

        self._zindex.register(zindex) # ensure unique z-index

        @typechecked
        def decorator(method: Callable) -> LayerABC:

            return Layer(
                method = method,
                zindex = zindex,
                video = self,
                canvas = canvas,
                offset = offset,
            ) # callable object (pretending to be a method)

        return decorator

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CANVAS PROTOTYPES FOR LAYER
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def canvas(self, canvas: str = 'drawingboard', **kwargs) -> Callable:

        return inventory[canvas].prototype(video = self, **kwargs)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# RENDER VIDEO
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def render(self,
        processes: int = 1,
        batchsize: int = 256,
        buffersize: int = 134217728,
        frame_fn: Union[str, None] = None,
        video_fn: Union[str, None] = None,
        ):

        assert 0 < processes
        assert 0 < batchsize
        assert 0 < buffersize

        self.reset()

        workers = mp.Pool(
            processes = processes,
            initializer = self._worker_init,
            initargs = (self,),
            maxtasksperchild = batchsize,
        )
        workers_promises = [
            workers.apply_async(
                func = self._worker_render_frame,
                args = (time, video_fn is not None, frame_fn),
                error_callback = self._worker_error,
            ) for time in Time.range(self.time(0), self._length)
        ]

        if video_fn is not None:
            codec = Popen([
                'ffmpeg',
                '-y', # force overwrite of output file
                '-framerate', f'{self.fps:d}',
                '-f', 'image2pipe', # force input format
                '-i', '-', # data from stdin
                '-vcodec', 'bmp', # input codec
                '-s:v', f'{self._width:d}x{self._height:d}',
                '-c:v', 'libx264',
                '-preset', 'veryslow',
                '-crf', '0',
                video_fn,
            ],
            stdin = PIPE, stdout = DEVNULL, stderr = DEVNULL,
            bufsize = buffersize,
            )

        for promise in tqdm(workers_promises):
            frame = promise.get()
            if video_fn is None:
                continue
            frame.save(codec.stdin, 'bmp')
            codec.stdin.flush()
            frame.close()

        workers.close()
        workers.terminate()
        workers.join()

        if video_fn is None:
            return

        codec.stdin.close()
        codec.wait()

    def render_frame(self,
        time: Time,
        return_frame: bool,
        frame_fn: Union[str, None] = None,
        ) -> Union[PIL_Image.Image, None]:

        for preptask in self._preptasks:
            if time in preptask.sequence:
                preptask(time)

        layers = [
            layertask(time)
            for layertask in self._layertasks
            if time in layertask.sequence # only render layer if time within sequence
        ] # call layer render functions, get list of uni-size PIL images
        assert len(layers) != 0

        base_layer = PIL_Image.new('RGBA', (self._width, self._height), (0, 0, 0, 0)) # transparent black
        for layer in layers:
            base_layer.paste(im = layer, box = layer.offset, mask = layer)

        base_layer = base_layer.convert('RGB') # go from RGBA to RGB

        if frame_fn is not None:
            base_layer.save(frame_fn.format(index = time.index))

        if return_frame:
            return base_layer # for direct to video

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# WORKER INFRASTRUCTURE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @staticmethod
    def _worker_error(err: Exception):

        raise err

    @staticmethod
    def _worker_init(video: VideoABC):

        _workers[mp.current_process().name] = video

    @staticmethod
    def _worker_render_frame(*args, **kwargs): # transparent wrapper for `render_frame`

        return _workers[mp.current_process().name].render_frame(*args, **kwargs)
