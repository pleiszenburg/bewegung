# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/encoders.py: Wrapper for video encoders

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

from types import TracebackType
from typing import BinaryIO, Dict, Union, Type
from subprocess import Popen, PIPE, DEVNULL

from .abc import EncoderABC, VideoABC
from .const import (
    PIPE_BUFFER_DEFAULT,
    FFMPEG_CRF_DEFAULT,
    FFMPEG_PRESET_DEFAULT,
    FFPMEG_TUNE_DEFAULT,
    )
from .typeguard import typechecked

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: BASE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class BaseEncoder(EncoderABC):
    """
    Mutable. Context manager. Wraps video envoders.

    Args:
        width : Video width in pixels
        height : Video width in pixels
        fps : Frames per second
        video_fn : Location and name (path) of where to store the video file.
            If omitted, no video will be rendered.
            However, indivual frames may in fact still be rendered if ``frame_fn`` has been specified.
    """

    def __init__(self,
        width: int,
        height: int,
        fps: int,
        video_fn: str,
    ):

        if width <= 0:
            raise ValueError('width must be greater than 0')
        if height <= 0:
            raise ValueError('height must be greater than 0')
        if fps <= 0:
            raise ValueError('fps must be greater than 0')

        if len(video_fn) == 0:
            raise ValueError('video_fn must not be empty')

        self._width, self._height, self._fps = width, height, fps
        self._video_fn = video_fn

        self._running = False
        self._stream = None

    def __repr__(self) -> str:

        return f'<{type(self).__name__} width={self._width:d} height={self._height:d} fps={self._fps:d} video_fn="{self._video_fn:s}" running={"yes" if self._running else "no"}>'

    @property
    def stream(self) -> BinaryIO:

        if not self._running:
            raise RuntimeError('encoder is not running')

        return self._stream

    @property
    def video_fn(self) -> str:

        return self._video_fn

    @video_fn.setter
    def video_fn(self, value: str):

        if self._running:
            raise RuntimeError('encoder is currently running')
        if len(value) == 0:
            raise ValueError('video_fn must not be empty')

        self._video_fn = value

    def __enter__(self) -> BinaryIO:

        raise NotImplementedError()

    def __exit__(
        self,
        exc_type: Union[Type, None],
        exc_value: Union[Exception, None],
        traceback: Union[TracebackType, None],
    ):

        raise NotImplementedError()

    @classmethod
    def from_video(cls, *args, **kwargs) -> EncoderABC:

        return cls(**cls._from_video(*args, **kwargs))

    @classmethod
    def _from_video(cls, video: VideoABC, video_fn: str) -> Dict:

        return dict(
            width = video.width,
            height = video.height,
            fps = video.fps,
            video_fn = video_fn,
        )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES: ENCODERS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class FFmpegEncoder(BaseEncoder):
    """
    Mutable. Context manager. Wraps FFmpeg.

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
        *args,
        buffersize: int = PIPE_BUFFER_DEFAULT,
        preset: str = FFMPEG_PRESET_DEFAULT,
        crf: int = FFMPEG_CRF_DEFAULT,
        tune: str = FFPMEG_TUNE_DEFAULT,
        **kwargs,
    ):

        super().__init__(*args, **kwargs)

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

    def __enter__(self) -> BinaryIO:

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
        self._stream = self._proc.stdin
        self._running = True

        return self.stream

    def __exit__(
        self,
        exc_type: Union[Type, None],
        exc_value: Union[Exception, None],
        traceback: Union[TracebackType, None],
    ):

        self._running = False

        self._proc.stdin.flush()
        self._proc.stdin.close()
        self._proc.wait()

        self._proc = None
        self._stream = None

    @classmethod
    def from_video(cls,
        *args,
        buffersize: int = PIPE_BUFFER_DEFAULT,
        preset: str = FFMPEG_PRESET_DEFAULT,
        crf: int = FFMPEG_CRF_DEFAULT,
        tune: str = FFPMEG_TUNE_DEFAULT,
        **kwargs,
    ) -> EncoderABC:

        return cls(
            **cls._from_video(*args, **kwargs),
            buffersize = buffersize,
            preset = preset,
            crf = crf,
            tune = tune,
        )
