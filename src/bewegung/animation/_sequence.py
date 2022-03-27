# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_sequence.py: Video Sequence

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

from typing import Dict

from ..lib import typechecked
from ._abc import SequenceABC, TimeABC, VideoABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Sequence(SequenceABC):
    """
    Holds layers and prepare tasks. "Base class" for user-defined sequences.
    Actually, new classes are created by making this class inherit from user-defined sequence classes.
    Do not instantiate this class or derive from it - use the :meth:`bewegung.Video.sequence` decorator instead!

    Mutable.

    Args:
        start : Begin of sequence within video
        stop : End of sequence within video
        video : Parent video object
    """

    def __init__(self, start: TimeABC, stop: TimeABC, video: VideoABC):

        # consistency checks are performed in Video.sequence

        self._start, self._stop = start, stop
        self._video, self._ctx = video, video.ctx

        self._length = stop - start

    def __repr__(self) -> str:

        return f'<Sequence name={type(self).__name__:s}>'

    def __len__(self) -> int:
        """
        Duration of sequence as number of frames
        """

        return self._length.index

    def __contains__(self, time: TimeABC) -> bool:
        """
        Checks whether a ``Time`` is within the sequence.

        Args:
            time : Time within parent video
        """

        return self._start <= time and time < self._stop

    def reset(self):
        """
        Calls the constructor of the user-defined sequence class.
        Used to reset the sequence for a (new) rendering run.
        """

        super().__init__()

    @property
    def length(self) -> TimeABC:
        """
        Duration of sequence
        """

        return self._length

    @property
    def start(self) -> TimeABC:
        """
        Begin of sequence within video
        """

        return self._start

    @property
    def stop(self) -> TimeABC:
        """
        End of sequence within video
        """

        return self._stop

    @property
    def video(self) -> VideoABC:
        """
        "Parent" video object
        """

        return self._video

    @property
    def ctx(self) -> Dict:
        """
        "Parent" context dictionary
        """

        return self._ctx
