# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/video_old.py: Parallel video frame renderer

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
import typing

import tqdm
from typeguard import typechecked

from .abc import SequenceABC, VideoABC
from .time import Time

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# "GLOBALS" (FOR WORKERS)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

_context = {}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: Sequence
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Sequence(SequenceABC):
    """
    Renders a number of layers with a z-index and provides them to a video.
    Can overlap with other sequences.
    """
    def __init__(self, start: Time, stop: Time, data: typing.Dict):
        if stop.index <= start.index:
            raise ValueError()
        self._start, self._stop, self._data = start, stop, data
    def __contains__(self, time: Time) -> bool:
        return self._start <= time and time < self._stop
    def get_prepare(self, time: Time) -> typing.Dict[int, typing.Callable]:
        return self._get(time = time, prefix = 'prepare_')
    def get_layer(self, time: Time) -> typing.Dict[int, typing.Callable]:
        return self._get(time = time, prefix = 'layer_')
    def _get(self, time: Time, prefix: str) -> typing.Dict[int, typing.Callable]:
        funcs = [
            getattr(self, attr)
            for attr in dir(self)
            if attr.startswith(prefix) and hasattr(getattr(self, attr), '__call__')
            ]
        items = {}
        for func in funcs:
            index, callback = func(time)
            if index in items.keys():
                raise ValueError()
            items[index] = callback
        return items

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: Video
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Video(VideoABC):
    """
    Main class for video rendering.
    """
    def __init__(self,
        time: Time,
        sequences: typing.List[Sequence],
        out_path: str = 'frame_{index:09d}.png',
        processes: int = mp.cpu_count(),
        fpp: int = 250, # frames per process
        ):
        if time.index <= 0:
            raise ValueError()
        self._time, self._sequences, self._out_path = time, sequences, out_path
        self._processes, self._fpp = processes, fpp
    def __repr__(self):
        return (
            f'<Video frames={self._time.index:d} length={self._time.time:.03f}s fps={self._time.fps:d} '
            + f'processes={self._processes:d} fpp={self._fpp:d}>'
        )
    def __len__(self):
        return self._time.index
    @property
    def out_path(self) -> str:
        return self._out_path
    @property
    def sequences(self) -> typing.List[Sequence]:
        return self._sequences.copy()
    def render(self):
        workers = mp.Pool(
            processes = self._processes,
            initializer = self._worker_init,
            initargs = (self,),
            maxtasksperchild = self._fpp,
        )
        workers_promises = [
            workers.apply_async(
                func = self._worker_render_frame,
                args = (time,),
                error_callback = self._worker_error,
            ) for time in Time.range(Time(fps = self._time.fps, index = 0), self._time)
            ]
        _ = [promise.get() for promise in tqdm.tqdm(workers_promises)]
    @staticmethod
    def _worker_error(err):
        raise err
    @staticmethod
    def _worker_init(video: VideoABC):
        _context[mp.current_process().name] = video
    @classmethod
    def _worker_render_frame(cls, time: Time):
        video = _context[mp.current_process().name]
        video.render_frame(time)
    def render_frame(self, time: Time):
        # PREPARE
        for prepare_func in self._get_funcs(time = time, get_name = 'get_prepare'):
            prepare_func()
        # RENDER
        layer_funcs = self._get_funcs(time = time, get_name = 'get_layer')
        if len(layer_funcs) == 0:
            raise ValueError()
        base_layer_pil = layer_funcs.pop(0)()
        for layer_func in layer_funcs:
            layer_pil = layer_func()
            base_layer_pil.paste(im = layer_pil, mask = layer_pil)
        base_layer_pil.convert('RGB').save(self.out_path.format(index = time.index))
    def _get_funcs(self, time: Time, get_name: str) -> typing.List[typing.Callable]:
        funcs = {}
        for sequence in self.sequences:
            if time not in sequence:
                continue
            new_funcs = getattr(sequence, get_name)(time)
            if len(new_funcs.keys() & funcs.keys()) != 0:
                raise ValueError()
            funcs.update(new_funcs)
        return [funcs[index] for index in sorted(funcs.keys())]
