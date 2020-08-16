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

import multiprocessing as mp
from subprocess import Popen, PIPE
from typing import Callable, Dict, Union, Tuple

from cairo import FORMAT_ARGB32, ImageSurface, Format
from datashader import Canvas
from datashader.transfer_functions import Image as DS_Image
from PIL import Image as PIL_Image, ImageOps as PIL_ImageOps
from tqdm import tqdm
from typeguard import typechecked

from .abc import CanvasTypes, SequenceABC, VideoABC
from .drawingboard import DrawingBoard
from .indexpool import IndexPool
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

        self._preptasks = [] # list of sequence prepare tasks
        self._layertasks = [] # list of layer render tasks
        self._preporder = IndexPool()
        self._zindex = IndexPool()

    def __repr__(self) -> str:

        return f'<Video frames={self._time.index:d} length={self._time.time:.03f}s fps={self._time.fps:d}>'

    def __len__(self) -> int:

        return self._time.index

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
    def preporder(self) -> IndexPool:
        return self._preporder

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
                def __init__(other):
                    other._start, other._stop = start, stop
                    other._video, other._ctx = self, self._ctx
                    super().__init__()
                def __repr__(other) -> str:
                    return f'<Sequence name={cls.__name__:s}>'
                def __contains__(other, time: Time) -> bool:
                    return other._start <= time and time < other._stop
                @property
                def start(other) -> Time:
                    return other._start
                @property
                def stop(other) -> Time:
                    return other._stop
                @property
                def video(other) -> VideoABC:
                    return other._video
                @property
                def ctx(other) -> Dict:
                    return other._ctx

            self._sequences.append((wrapper, None)) # track sequence classes and objects
            return None # wrapper # HACK remove original class?

        return decorator

    def cairo_canvas(self, **kwargs):

        if 'format' not in kwargs.keys():
            kwargs['format'] = FORMAT_ARGB32
        if 'width' not in kwargs.keys():
            kwargs['width'] = self._width
        if 'height' not in kwargs.keys():
            kwargs['height'] = self._height

        return lambda: ImageSurface(kwargs['format'], kwargs['width'], kwargs['height'])

    def db_canvas(self, **kwargs):

        if 'width' not in kwargs.keys():
            kwargs['width'] = self._width
        if 'height' not in kwargs.keys():
            kwargs['height'] = self._height

        return lambda: DrawingBoard(**kwargs)

    def ds_canvas(self, **kwargs):

        if 'plot_width' not in kwargs.keys():
            kwargs['plot_width'] = self._width
        if 'plot_height' not in kwargs.keys():
            kwargs['plot_height'] = self._height

        if 'x_range' not in kwargs.keys():
            kwargs['x_range'] = (0, self._width)
        if 'y_range' not in kwargs.keys():
            kwargs['y_range'] = (0, self._height)

        return lambda: Canvas(**kwargs)

    def pil_canvas(self, **kwargs):

        if 'mode' not in kwargs.keys():
            kwargs['mode'] = 'RGBA'
        if 'size' not in kwargs.keys():
            kwargs['size'] = (self._width, self._height)

        return lambda: PIL_Image.new(**kwargs)

    def prepare(self,
        preporder: int,
    ) -> Callable:

        self._preporder.register(preporder) # ensure unique preporder

        @typechecked
        def decorator(func: Callable) -> Callable:

            @typechecked
            def wrapper(other, time: Time): # other is the current sequence

                kwargs = {}
                for param in func.__code__.co_varnames: # parameters requested by user
                    if param == 'time':
                        kwargs[param] = time
                    elif param == 'reltime':
                        kwargs[param] = time - other.start
                    elif param == 'self':
                        continue
                    else:
                        raise ValueError('unknown parameter')

                func(other, **kwargs) # let user draw layer/canvas for frame

            wrapper.preporder_tag = preporder # tag wrapper function
            return wrapper

        return decorator

    def layer(self,
        zindex: int,
        canvas: Union[Callable[[], CanvasTypes], None],
        box: Tuple[int, int] = (0, 0),
    ) -> Callable:

        self._zindex.register(zindex) # ensure unique z-index

        if canvas is None:
            canvas = self.db_canvas()

        @typechecked
        def decorator(func: Callable) -> Callable:

            @typechecked
            def wrapper(other, time: Time) -> PIL_Image.Image: # other is the current sequence

                kwargs = {}
                for param in func.__code__.co_varnames: # parameters requested by user
                    if param == 'time':
                        kwargs[param] = time
                    elif param == 'reltime':
                        kwargs[param] = time - other.start
                    elif param == 'canvas':
                        if canvas is not None:
                            kwargs[param] = canvas()
                        else:
                            raise ValueError('no canvas type defined')
                    elif param == 'self':
                        continue
                    else:
                        raise ValueError('unknown parameter')

                cvs = func(other, **kwargs) # let user draw layer/canvas for frame

                if isinstance(cvs, PIL_Image.Image):
                    assert cvs.mode == 'RGBA'
                elif isinstance(cvs, DS_Image):
                    cvs = cvs.to_pil()
                    assert cvs.mode == 'RGBA'
                    cvs = PIL_ImageOps.flip(cvs) # datashader's y axis must be flipped
                elif isinstance(cvs, DrawingBoard):
                    cvs = cvs.as_pil()
                elif isinstance(cvs, ImageSurface):
                    assert cvs.get_format() == Format.ARGB32
                    cvs = PIL_Image.frombuffer(
                        mode = 'RGBA',
                        size = (cvs.get_width(), cvs.get_height()),
                        data = cvs.get_data(),
                        )
                else:
                    raise TypeError('unknown canvas type coming from layer')

                cvs.box = box # annotate offset for later use

                return cvs

            wrapper.zindex_tag = zindex # tag wrapper function
            return wrapper

        return decorator

    # TODO "after effects" - similar to "layer"

    def render(self,
        processes: int = 1,
        batchsize: int = 256,
        frame_fn: Union[str, None] = None,
        video_fn: Union[str, None] = None,
        ):

        assert 0 < processes <= mp.cpu_count()
        assert 0 < batchsize

        self._sequences[:] = [(cls, cls()) for cls, _ in self._sequences] # (re-)init sequences, keep class

        self._preptasks.clear()
        self._preptasks.extend([
            Task(
                sequence = sequence,
                index = getattr(sequence, attr).preporder_tag,
                task = getattr(sequence, attr),
            )
            for _, sequence in self._sequences for attr in dir(sequence)
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
            for _, sequence in self._sequences for attr in dir(sequence)
            if hasattr(getattr(sequence, attr), 'zindex_tag')
        ]) # find layer methods based on tags
        self._layertasks.sort() # sort by (z-) index

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
            ) for time in Time.range(Time(fps = self._time.fps, index = 0), self._time)
        ]

        if video_fn is not None:
            codec = Popen([
                'ffmpeg',
                '-y', # force overwrite of output file
                '-framerate', f'{self._time.fps:d}',
                '-f', 'image2pipe', # force input format
                '-i', '-', # data from stdin
                '-vcodec', 'bmp', # input codec
                '-s:v', f'{self._width:d}x{self._height:d}',
                '-c:v', 'libx264',
                '-preset', 'veryslow',
                '-crf', '0',
                video_fn,
            ], stdin = PIPE, stdout = PIPE, stderr = PIPE,)

        for promise in tqdm(workers_promises):
            frame = promise.get()
            if video_fn is None:
                continue
            frame.save(codec.stdin, 'bmp')

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
            base_layer.paste(im = layer, box = layer.box, mask = layer)

        base_layer = base_layer.convert('RGB') # go from RGBA to RGB

        if frame_fn is not None:
            base_layer.save(frame_fn.format(index = time.index))

        if return_frame:
            return base_layer # for direct to video

    @staticmethod
    def _worker_error(err: Exception):

        raise err

    @staticmethod
    def _worker_init(video: VideoABC):

        _workers[mp.current_process().name] = video

    @staticmethod
    def _worker_render_frame(*args, **kwargs): # transparent wrapper for `render_frame`

        return _workers[mp.current_process().name].render_frame(*args, **kwargs)
