# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/core/effects.py: Video frame effects

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

from PIL import Image as PIL_Image
from typeguard import typechecked

from .abc import SequenceABC, TimeABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
def fade_in(
    blend_time: TimeABC,
) -> Callable:

    @typechecked
    def decorator(func: Callable) -> Callable:

        @typechecked
        def wrapper(sequence: SequenceABC, time: TimeABC) -> PIL_Image.Image:

            cvs = func(sequence, time)

            reltime = time - sequence.start
            if reltime > blend_time:
                return cvs

            r, g, b, a = cvs.split()
            factor = reltime.index / blend_time.index
            a = a.point(lambda i: i * factor)
            new_cvs = PIL_Image.merge('RGBA', (r, g, b, a))

            new_cvs.box = cvs.box # maintain tag
            return new_cvs

        wrapper.zindex_tag = func.zindex_tag # maintain tag
        return wrapper

    return decorator

@typechecked
def fade_out(
    blend_time: TimeABC,
) -> Callable:

    @typechecked
    def decorator(func: Callable) -> Callable:

        @typechecked
        def wrapper(sequence: SequenceABC, time: TimeABC) -> PIL_Image.Image:

            cvs = func(sequence, time)

            if time < sequence.stop - blend_time:
                return cvs
            nreltime = sequence.stop - time

            r, g, b, a = cvs.split()
            factor = nreltime.index / blend_time.index
            a = a.point(lambda i: i * factor)
            new_cvs = PIL_Image.merge('RGBA', (r, g, b, a))

            new_cvs.box = cvs.box # maintain tag
            return new_cvs

        wrapper.zindex_tag = func.zindex_tag # maintain tag
        return wrapper

    return decorator
