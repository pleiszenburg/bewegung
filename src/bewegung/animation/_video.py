# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_video.py: Parallel video frame renderer

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

import inspect
import multiprocessing as mp
from typing import Callable, Dict, Union

from PIL import Image as PIL_Image
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    tqdm = lambda x: x

from ..lib import typechecked
from ..linalg import Vector2D
from ._abc import EncoderABC, LayerABC, SequenceABC, VideoABC, TimeABC
from ._backends import backends
from ._const import FPS_DEFAULT
from ._encoders import FFmpegH264Encoder
from ._indexpool import IndexPool
from ._layer import Layer
from ._sequence import Sequence
from ._task import Task
from ._time import Time

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
    This class is the "core" of ``bewegung``.
    It generates *video objects*.
    They manage *sequences*, *layer tasks* and *prepare tasks*
    Video objects are also responsible for rendering actual video files and individual frames.

    Video objects are mutable.

    Args:
        width : Video width in pixels
        height : Video width in pixels
        ctx : Context, store for any type of video context data
        fps : Frames per second
        seconds : Duration of video in seconds (``frames`` and ``seconds`` are mutually exclusive. Specify excactly one of two.)
        frames : Duration of video as number of frames (``frames`` and ``seconds`` are mutually exclusive. Specify excactly one of two.)
    """

    def __init__(self,
        width: int,
        height: int,
        ctx: Union[Dict, None] = None,
        fps: int = FPS_DEFAULT,
        seconds: Union[float, int, None] = None,
        frames: Union[int, None] = None,
    ):

        if width <= 0:
            raise ValueError('width must be greater than 0')
        if height <= 0:
            raise ValueError('height must be greater than 0')

        self._width = width
        self._height = height
        self._ctx = ctx if ctx is not None else {}

        if fps <= 0:
            raise ValueError('fps must be greater than 0')
        if not ((seconds is not None) ^ (frames is not None)):
            raise ValueError('frames and seconds are mutually exclusive')
        if seconds is not None:
            if seconds <= 0:
                raise ValueError('seconds must be greater than 0')
        if frames is not None:
            if frames <= 0:
                raise ValueError('frames must be greater than 0')
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
        """
        String representation for interactive use
        """

        return f'<Video frames={self._length.index:d} seconds={self._length.seconds:.03f}s fps={self.fps:d}>'

    def __len__(self) -> int:
        """
        Duration of video as number of frames
        """

        return self._length.index

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PROPERTIES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @property
    def length(self) -> TimeABC:
        """
        Duration of video
        """

        return self._length

    @property
    def fps(self) -> int:
        """
        Frames per second
        """

        return self._length.fps

    @property
    def width(self) -> int:
        """
        Width of video in pixels
        """

        return self._width

    @property
    def height(self) -> int:
        """
        Height of video in pixels
        """

        return self._height

    @property
    def ctx(self) -> Dict:
        """
        Context (mutable), store for any type of video context data
        """

        return self._ctx

    @property
    def preporder(self) -> IndexPool:
        """
        Prepare-order :class:`bewegung.IndexPool` object for prepare tasks (mutable)
        """

        return self._preporder

    @property
    def zindex(self) -> IndexPool:
        """
        Z-index :class:`bewegung.IndexPool` object for layers (mutable)
        """

        return self._zindex

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# RESET TASKS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def time(self, index: int) -> TimeABC:
        """
        Generates a new :class:`bewegung.Time` object from a given number of frames based on the video's frames per second.

        Args:
            index : Number of frames
        """

        return self._length.time(index = index)

    def time_from_seconds(self, seconds: Union[float, int]) -> TimeABC:
        """
        Generates a new :class:`bewegung.Time` object from a given time in seconds based on the video's frames per second.

        Args:
            seconds : Time in seconds
        """

        return self._length.time_from_seconds(seconds = seconds)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# RESET TASKS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def reset(self):
        """
        This method allows to reset a video object in preparation of a new render run.
        It is automatically invoked when calling :meth:`bewegung.Video.render`.
        It may instead be used before rendering indivual frames with :meth:`bewegung.Video.render_frame`.
        """

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
        length: Union[Time, None] = None,
    ) -> Callable:
        """
        A **decorator** for decorating user-defined ``sequence`` classes.
        New classes are created by making :class:`bewegung.core.sequence.Sequence` inherit from the user-defined sequence classes.

        Args:
            start : Time of start of sequence within the video.
                A negative time can be used to specify a time relative to the end of the video.
                Defaults to the beginning of the video.
            stop : Time of stop of sequence within the video.
                A negative time can be used to specify a time relative to the end of the video.
                Defaults to the end of the video.
                ``stop`` and ``length`` are mutually exclusive. Specify one at most.
            length : Length of the sequence.
                ``stop`` and ``length`` are mutually exclusive. Specify one at most.
        """

        if start is None:
            start = self.time(0)
        if start.fps != self.fps:
            start = self.time_from_seconds(seconds = start.seconds)

        if stop is not None and length is not None:
            raise ValueError('stop and length are mutually exclusive')
        if length is not None:
            if length.fps != length.fps:
                length = self.time_from_seconds(seconds = length.seconds)
            stop = length - start
        if stop is not None:
            if stop.fps != self.fps:
                stop = self.time_from_seconds(seconds = stop.seconds)
        else:
            stop = self._length

        if start < self.time(0):
            start = self._length + start
        if not (self.time(0) <= start <= self._length):
            raise ValueError('start out of bounds')
        if stop < self.time(0):
            stop = self._length + stop
        if not (self.time(0) <= stop <= self._length):
            raise ValueError('stop out of bounds')

        if start >= stop:
            raise ValueError('stop smaller or equal to stop')

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
        preporder: Union[int, None] = None,
    ) -> Callable:
        """
        A **decorator** for decorating ``prepare`` methods (tasks) within ``sequence`` classes.

        Args:
            preporder : A number, managed by an :class:`bewegung.IndexPool` object (:attr:`bewegung.Video.preporder`),
                representing the relative position within a set of ``prepare`` tasks.
                If not provided, the new task will be created at the end of the set.
        """

        if preporder is None:
            preporder = self._preporder.on_top()

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
        zindex: Union[int, None] = None,
        canvas: Union[Callable, None] = None,
        offset: Union[Vector2D, None] = None,
    ) -> Callable:
        """
        A **decorator** for decorating ``layer`` methods (tasks) within ``sequence`` classes.
        Methods are wrapped with callable :class:`bewegung.core.layer.Layer` objects.

        Args:
            zindex : A number, managed by an :class:`bewegung.IndexPool` object (:attr:`bewegung.Video.zindex`),
                representing the relative position within a stack of ``layer`` tasks.
                If not provided, the new layer will be created on top.
            canvas : A function pointer to a factory function, generating a new canvas once per frame for the ``layer`` task.
                The pointer is typically generated by the :meth:`bewegung.Video.canvas` method.
            offset : The layer's offset relative to the top-left corner of the video. The y-axis is downwards positive.
        """

        if offset is None:
            offset = Vector2D(0, 0)
        if zindex is None:
            zindex = self._zindex.on_top()

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

    def canvas(self, backend: str = 'drawingboard', **kwargs) -> Callable:
        """
        A method to create function pointers to factory functions generating new canvases.
        The pointers can be passed to the ``canvas`` parameter in the :meth:`bewegung.Video.layer` decorator method.

        Args:
            backend : Selected type of canvas, i.e. name of desired :ref:`backend <drawing>`.
            kwargs : Keyword arguments of the selected backend's canvas creation function.
        """

        return backends[backend].prototype(video = self, **kwargs)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# RENDER VIDEO
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def render(self,
        processes: int = 1,
        batchsize: int = 256,
        encoder: Union[EncoderABC, None] = None,
        frame_fn: Union[str, None] = None,
        video_fn: Union[str, None] = None,
        ):
        """
        A method for rendering the actual video file.

        This function starts at least one Python sub-process (worker process) for rendering frames.
        Based on multiple worker processes, multiple frames can be rendered in parallel.
        If a filename for a video is specified, the rendered frames are streamed to a video encoder.

        Args:
            processes : Number of parallel frame rendering (worker) processes
            batchsize : Maximum number of frames rendered by a worker process before the (old) worker is replaced by a new worker.
                This option helps to prevent long rendering jobs from running out of memory.
            encoder : A video encoder object.
                If omitted, a :class:`bewegung.FFmpegH264Encoder` object will generated and used.
            frame_fn : A Python string (representing a path) including an integer `replacement field`_ called ``index``.
                If specified, individual frames will be stored here.
                If omitted, no frames will be stored.
            video_fn: Location and name (path) of where to store the video file.
                If omitted, no video will be rendered.
                However, indivual frames may in fact still be rendered if ``frame_fn`` has been specified.

        .. _replacement field: https://docs.python.org/3/library/stdtypes.html#str.format
        """

        if processes <= 0:
            raise ValueError('processes must be greater than 0')
        if batchsize <= 0:
            raise ValueError('batchsize must be greater than 0')

        if video_fn is not None and len(video_fn) == 0:
            raise ValueError('if a string, video_fn must not be empty')
        if video_fn is not None and encoder is None:
            encoder = FFmpegH264Encoder()

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

        if video_fn is None:

            for promise in tqdm(workers_promises):
                _ = promise.get()

        else:

            with encoder(video = self, video_fn = video_fn) as stream:
                for promise in tqdm(workers_promises):
                    frame = promise.get()
                    frame.save(stream, 'bmp')
                    stream.flush()
                    frame.close()

        workers.close()
        workers.terminate()
        workers.join()

    def render_frame(self,
        time: Time,
        return_frame: bool = True,
        frame_fn: Union[str, None] = None,
        ) -> Union[PIL_Image.Image, None]:
        """
        A method for rendering individual frames of the video.

        The frames can optionally be written to disk and/or returned to the caller.
        **Before calling this method for the first time,** :meth:`bewegung.Video.reset` **must be invoked!**

        Args:
            time : Time of the frame relative to the beginning of the video
            return_frame : If ``True``, the frame is returned to the caller of the method.
            frame_fn: Location and name (path) of where to store the rendered frame.
                If omitted, the frame is not stored.
        Returns:
            If requested via ``return_frame``, a pillow image object is returned.
        """

        for preptask in self._preptasks:
            if time in preptask.sequence:
                preptask(time)

        layers = [
            layertask(time)
            for layertask in self._layertasks
            if time in layertask.sequence # only render layer if time within sequence
        ] # call layer render functions, get list of uni-size PIL images

        base_layer = PIL_Image.new('RGBA', (self._width, self._height), (0, 0, 0, 0)) # transparent black
        for layer in layers:
            base_layer.paste(im = layer, box = layer.offset.as_tuple(), mask = layer)

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
