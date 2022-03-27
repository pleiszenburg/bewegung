# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_encoders.py: Wrapper for video encoders

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

from types import TracebackType
from typing import BinaryIO, Union, Type
from subprocess import Popen, PIPE, DEVNULL

from ..lib import typechecked
from ._abc import EncoderABC, VideoABC
from ._const import (
    PIPE_BUFFER_DEFAULT,
    FFMPEG_CRF_DEFAULT,
    FFMPEG_PRESET_DEFAULT,
    FFPMEG_TUNE_DEFAULT,
    )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: BASE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class EncoderBase(EncoderABC):
    """
    Encoder classes wrap video encoding tools and libraries such as ``ffmpeg``.
    Encoder objects are callable and return themselves when called. This mechanism is used to (re-) configure the encoder object.
    Encoder objects also use Python's context manager protocol and expose ``BinaryIO`` objects, i.e. streams, as a context for actual encoding.
    :meth:`bewegung.Video.render` will write rendered images as RGB bitmaps to this stream so the encoder can pick them up.
    Encoder objects can either be "running" or "idling". They can also either be "configured" or "unconfigured".
    In the latter case, they will not allow to encode a video.

    Mutable.

    If the orginal cunstructor method is overridden, it must be called from the child class.
    """

    def __init__(self):

        self._width = None
        self._height = None
        self._fps = None
        self._video_fn = None
        self._stream = None

    def __call__(self, video: VideoABC, video_fn: str) -> EncoderABC:
        """
        Configures the encoder. Returns encoder object itself.

        Do not override!

        Args:
            video : Video object
            video_fn : Location and name (path) of where to store the video file.
                If omitted, no video will be rendered.
                However, indivual frames may in fact still be rendered if ``frame_fn`` has been specified.
        """

        if len(video_fn) == 0:
            raise ValueError('video_fn must not be empty')

        self._width = video.width
        self._height = video.height
        self._fps = video.fps
        self._video_fn = video_fn

        return self

    def __repr__(self) -> str:

        return f'<{type(self).__name__} configured={"yes" if self.configured else "no"} running={"yes" if self.running else "no"}>'

    @property
    def configured(self) -> bool:
        """
        Has the encoder been configured?

        Do not override!
        """

        return self._video_fn is not None

    @property
    def running(self) -> bool:
        """
        Is the encoder currently running?

        Do not override!
        """

        return self._stream is not None

    @property
    def stream(self) -> BinaryIO:
        """
        Exposes the input stream of the encoder.
        If the encoder is not running, trying to access this attribute raises an exception.

        Do not override!
        """

        if not self.running:
            raise RuntimeError('encoder is not running')

        return self._stream

    @property
    def video_fn(self) -> str:
        """
        Exposes the name/path of the target video file.
        If the encoder is not configured, trying to access this attribute raises an exception.

        Do not override!
        """

        if not self.configured:
            raise RuntimeError('encoder is not configured')

        return self._video_fn

    @video_fn.setter
    def video_fn(self, value: str):
        """
        Exposes the name/path of the target video file.
        If the encoder is not configured, trying to access this attribute raises an exception.

        Do not override!
        """

        if not self.configured:
            raise RuntimeError('encoder is not configured')
        if self.running:
            raise RuntimeError('encoder is currently running')
        if len(value) == 0:
            raise ValueError('video_fn must not be empty')

        self._video_fn = value

    def __enter__(self) -> BinaryIO:
        """
        Context manager entry point. Returns the encoder's input stream.

        Do not override!
        """

        if not self.configured:
            raise RuntimeError('encoder has not been configured')
        if self.running:
            raise RuntimeError('encoder is already running')

        self._stream = self._enter()
        return self._stream

    def _enter(self) -> BinaryIO:
        """
        Starts the encoder. Returns the encoder's input stream.

        Must be reimplemented!
        """

        raise NotImplementedError()

    def __exit__(
        self,
        exc_type: Union[Type, None],
        exc_value: Union[Exception, None],
        traceback: Union[TracebackType, None],
    ):
        """
        Context manager exit point.

        Do not override!

        Args:
            exc_type : Type of exception
            exc_value : Actual exception object
            traceback : Related traceback object
        """

        if not self.running:
            raise RuntimeError('encoder is not running')

        self._stream = None
        self._exit()

    def _exit(self):
        """
        Stops the encoder.

        Must be reimplemented!
        """

        raise NotImplementedError()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES: ENCODERS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class FFmpegH264Encoder(EncoderBase):
    """
    Mutable. Context manager. Wraps FFmpeg with H.264.

    Args:
        buffersize : Maximum size of buffer in bytes between ``bewegung`` and ``ffmpeg``.
            A larger buffer may have a mildly positive impact on performance.
        preset : ``ffmpeg`` encoding and compression preset. See `ffmpeg's H.264 preset documentation`_ for details.
        crf : ``ffmpeg`` Constant Rate Factor (CRF) value. See `ffmpeg's H.264 CRF documentation`_ for details.
        tune : ``ffmpeg`` tune option. See `ffmpeg's H.264 tune documentation`_ for details.

    .. _`ffmpeg's H.264 preset documentation`: https://trac.ffmpeg.org/wiki/Encode/H.264#Preset
    .. _`ffmpeg's H.264 CRF documentation`: https://trac.ffmpeg.org/wiki/Encode/H.264#crf
    .. _`ffmpeg's H.264 tune documentation`: https://trac.ffmpeg.org/wiki/Encode/H.264#Tune
    """

    def __init__(self,
        buffersize: int = PIPE_BUFFER_DEFAULT,
        preset: str = FFMPEG_PRESET_DEFAULT,
        crf: int = FFMPEG_CRF_DEFAULT,
        tune: str = FFPMEG_TUNE_DEFAULT,
    ):

        super().__init__()

        if buffersize <= 0:
            raise ValueError('buffersize must be greater than 0')
        if preset not in (
            "ultrafast",
            "superfast",
            "veryfast",
            "faster",
            "fast",
            "medium",
            "slow",
            "slower",
            "veryslow",
            ):
            raise ValueError('unknown ffmpeg preset')
        if not (0 <= crf <= 51):
            raise ValueError('ffmpeg crf out of bounds')
        if tune not in (
            "film",
            "animation",
            "grain",
            "stillimage",
            "fastdecode",
            "zerolatency",
            ):
            raise ValueError('unknown ffmpeg tune')

        self._buffersize = buffersize
        self._preset = preset
        self._crf = crf
        self._tune = tune

        self._proc = None

    def _enter(self) -> BinaryIO:

        self._proc = Popen(
            [
                'ffmpeg',
                '-y', # force overwrite of output file
                '-framerate', f'{self._fps:d}',
                '-f', 'image2pipe', # force input format
                '-i', '-', # data from stdin
                '-vcodec', 'bmp', # input codec
                '-s:v', f'{self._width:d}x{self._height:d}',
                '-c:v', 'libx264',
                '-preset', self._preset,
                '-crf', f'{self._crf:d}',
                '-tune', self._tune,
                self._video_fn,
            ],
            stdin = PIPE, stdout = DEVNULL, stderr = DEVNULL,
            bufsize = self._buffersize,
        )

        return self._proc.stdin

    def _exit(self):

        self._proc.stdin.flush()
        self._proc.stdin.close()
        self._proc.wait()

        self._proc = None

@typechecked
class FFmpegGifEncoder(EncoderBase):
    """
    Mutable. Context manager. Wraps FFmpeg with gif.

    Args:
        buffersize : Maximum size of buffer in bytes between ``bewegung`` and ``ffmpeg``.
            A larger buffer may have a mildly positive impact on performance.
    """

    def __init__(self,
        buffersize: int = PIPE_BUFFER_DEFAULT,
    ):

        super().__init__()

        if buffersize <= 0:
            raise ValueError('buffersize must be greater than 0')

        self._buffersize = buffersize

        self._proc = None

    def _enter(self) -> BinaryIO:

        self._proc = Popen(
            [
                'ffmpeg',
                '-y', # force overwrite of output file
                '-framerate', f'{self._fps:d}',
                '-f', 'image2pipe', # force input format
                '-i', '-', # data from stdin
                '-vcodec', 'bmp', # input codec
                '-s:v', f'{self._width:d}x{self._height:d}',
                '-vf', 'split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse',
                '-c:v', 'gif',
                self._video_fn,
            ],
            stdin = PIPE, stdout = DEVNULL, stderr = DEVNULL,
            bufsize = self._buffersize,
        )

        return self._proc.stdin

    def _exit(self):

        self._proc.stdin.flush()
        self._proc.stdin.close()
        self._proc.wait()

        self._proc = None
