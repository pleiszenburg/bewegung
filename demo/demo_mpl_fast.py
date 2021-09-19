# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    demo/demo_mpl_fast.py: Package demo - matplotlib accelerated

    Copyright (C) 2020-2021 Sebastian M. Ernst <ernst@pleiszenburg.de>

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

import math

try:
    import psutil
    CPU_CORES = psutil.cpu_count(logical = False)
except ModuleNotFoundError: # fallback
    import multiprocessing
    CPU_CORES = multiprocessing.cpu_count() // 2 # assume HT
    CPU_CORES = 1 if CPU_CORES < 1 else CPU_CORES

from bewegung import (
    Color, Video,
    Vector2D,
    FadeInEffect, FadeOutEffect,
    )

from bewegung.drawingboard import DrawingBoard

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CONST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

SVG_LOGO = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   viewBox="0 0 170 170"
   width="170"
   height="170"
>
  <path
     style="fill:#b4b4b4;fill-opacity:1;"
     d="m 275.57824,185.64694 -154.01,-67.09663 135.11238,-99.828253 z"
     transform="rotate(-44.941938,124.56725,280.97355)" />
</svg>
""".encode('utf-8')

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def main():

    v = Video(
        width = 1920,
        height = 1080,
        seconds = 10.0,
        ctx = {
            'bg_color': Color(26, 26, 26),
            'bg_color_transparent': Color(26, 26, 26, 0),
            'fg_color': Color(255, 255, 255)
        },
    )

    @v.sequence()
    class Background:

        @v.layer(
            zindex = v.zindex.on_bottom(),
            canvas = v.canvas(background_color = v.ctx['bg_color']),
        )
        def empty(self, canvas):
            return canvas

    @v.sequence(
        start = v.time_from_seconds(1.0),
        stop = v.time_from_seconds(-1.0),
    )
    class MplAcceleratedDemo:

        def __init__(self):

            self._x = [idx / 20 for idx in range(len(v))]
            self._y = [math.sin(x) for x in self._x]

            self._fig = v.canvas(
                backend = 'matplotlib',
                background_color = v.ctx['bg_color_transparent'],
                managed = False,
            )()
            self._ax = self._fig.subplots()
            self._ax.set_facecolor(f'#{v.ctx["bg_color_transparent"].as_hex():s}')
            self._ax.tick_params(
                color = f'#{v.ctx["fg_color"].as_hex():s}',
                labelcolor = f'#{v.ctx["fg_color"].as_hex():s}',
            )

        @FadeInEffect(v.time_from_seconds(4.0))
        @FadeOutEffect(v.time_from_seconds(2.0))
        @v.layer(
            zindex = v.zindex.on_top(),
        )
        def something(self, time):

            self._ax.clear()
            self._ax.plot(self._x[:time.index], self._y[:time.index], color = '#FF0000FF')

            return self._fig

    @v.sequence(
        stop = v.time_from_seconds(3.0),
    )
    class Intro:

        def __init__(self):

            self._font = DrawingBoard.make_font('Arial', 40.0)

        @FadeInEffect(v.time_from_seconds(1.6))
        @FadeOutEffect(v.time_from_seconds(0.8))
        @v.layer(
            zindex = v.zindex.on_top(),
            canvas = v.canvas(background_color = v.ctx['bg_color_transparent'], height = 200),
            offset = Vector2D(20, 20),
        )
        def text(self, canvas):

            canvas.draw_text(
                text = 'bewegung - a versatile video renderer\nDEMO - MATPLOTLIB',
                point = Vector2D(0.0, 0.0),
                font = self._font,
                font_color = Color(180, 180, 180),
                anchor = 'tl',
            )

            return canvas

    @v.sequence(
        start = v.time_from_seconds(-5.0),
        stop = v.time_from_seconds(-1.0),
    )
    class Credits:

        def __init__(self):

            self._font = DrawingBoard.make_font('Arial', 40.0)

        @FadeInEffect(v.time_from_seconds(2.0))
        @FadeOutEffect(v.time_from_seconds(2.0))
        @v.layer(
            zindex = v.zindex.on_top(),
            canvas = v.canvas(background_color = v.ctx['bg_color_transparent'], height = 200),
            offset = Vector2D(-20, v.height - 20 - 200),
        )
        def text(self, canvas):

            canvas.draw_text(
                text = 'github.com/pleiszenburg/bewegung',
                point = Vector2D(v.width, 200),
                font = self._font,
                font_color = Color(180, 180, 180),
                alignment = 'r',
                anchor = 'br',
            )

            return canvas

    @v.sequence(
        start = v.time_from_seconds(-1.2),
    )
    class CreditsLogo:

        def __init__(self):

            self._svg = DrawingBoard.make_svg(raw = SVG_LOGO)
            self._font = DrawingBoard.make_font('Arial', 25.0)

        @FadeInEffect(v.time_from_seconds(0.8))
        @FadeOutEffect(v.time_from_seconds(0.3))
        @v.layer(
            zindex = v.zindex.on_top(),
            canvas = v.canvas(background_color = v.ctx['bg_color_transparent']),
        )
        def text(self, canvas):

            canvas.draw_svg(
                svg = self._svg,
                point = Vector2D(v.width / 2, v.height / 2 - 50),
                scale = 2.0,
                anchor = 'cc',
            )
            canvas.draw_text(
                text = 'pleiszenburg.de - Independent Scientific Services\n2020',
                point = Vector2D(v.width / 2, v.height / 2 + 135),
                font = self._font,
                font_color = Color(180, 180, 180),
                alignment = 'c',
                anchor = 'tc',
            )

            return canvas

    v.render(
        processes = CPU_CORES,
        video_fn = 'video_mpl_fast.mp4',
        )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ENTRY
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == '__main__':

    main()
