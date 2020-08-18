# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    demo.py: Package demo

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

import math

from bewegung import Camera, Color, Time, Video, Vector2D, Vector3D, VectorArray3D, fade_in, fade_out

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def main():

    v = Video(
        time = Time.from_time(fps = 60, time = 10.0),
        width = 1920,
        height = 1080,
        ctx = {
            'background_color': Color(26, 26, 26),
            'camera_dist': 30,
            'camera': Camera(
                position = Vector3D(30.0, 0, 0),
                direction = Vector3D(-1.0, 0, 0),
                planeOffset = Vector2D(1920 / 2, 1080 / 2),
                planeFactor = 1000.0,
            ),
        }
    )

    @v.sequence()
    class Background:

        @v.layer(
            zindex = v.zindex.on_bottom(),
            canvas = v.db_canvas(background_color = v.ctx['background_color']),
        )
        def empty(self, canvas):
            return canvas

    @v.sequence(
        start = Time.from_time(fps = 60, time = 1.0),
        stop = v.time - Time.from_time(fps = 60, time = 1.0),
    )
    class Sphere:

        def __init__(self):
            self._lines3d = [
                VectorArray3D.from_iterable([
                    Vector3D.from_geographic(10.0, float(lon), float(lat))
                    for lat in range(-90, 90 + 10, 10)
                ])
                for lon in range(-180, 180, 10)
            ]
            self._lines3d.extend([
                VectorArray3D.from_iterable([
                    Vector3D.from_geographic(10.0, float(lon), float(lat))
                    for lon in range(-180, 180 + 10, 10)
                ])
                for lat in range(-90 + 10, 90, 10)
            ])
            self._lines2d = None
            self._factor = None

        @v.prepare(
            preporder = v.preporder.on_bottom(),
        )
        def move_camera(self, time):
            angle = 2 * math.pi * time.time / 120.0
            position2d = Vector2D.from_polar(radius = v.ctx['camera_dist'], angle = angle)
            direction2d = Vector2D.from_polar(radius = 1.0, angle = math.pi + angle)
            v.ctx['camera'].position = Vector3D(x = position2d.x, y = position2d.y, z = 0.0)
            v.ctx['camera'].direction = Vector3D(x = direction2d.x, y = direction2d.y, z = 0.0)

        @v.prepare(
            preporder = v.preporder.on_top(),
        )
        def project(self):
            self._lines2d = [
                v.ctx['camera'].get_points(line3d).as_list()
                for line3d in self._lines3d
            ]
            self._lines2d = [
                (a, b)
                for line2d in self._lines2d
                for a, b in zip(line2d[:-1], line2d[1:])
            ]
            self._lines2d.sort(key = lambda item: item[0].dist, reverse = True)
            minimum = self._lines2d[0][0].dist
            maximum = self._lines2d[-1][0].dist
            self._factor = lambda x: (x - minimum) / (maximum - minimum)

        @fade_in(Time.from_time(fps = 60, time = 4.0))
        @fade_out(Time.from_time(fps = 60, time = 2.0))
        @v.layer(
            zindex = v.zindex.on_top(),
            canvas = v.db_canvas(background_color = Color(26, 26, 26, 0)),
        )
        def wiremesh(self, canvas):
            for line in self._lines2d:
                factor = self._factor(line[0].dist)
                gray = round(64 + 191 * factor)
                canvas.draw_polygon(
                    *line,
                    line_color = Color(gray, gray, gray),
                    line_width = 1.6 + 1.6 * factor,
                )
            return canvas

    v.render(
        processes = 1,
        # frame_fn = 'frames/frame_{index:07d}.png',
        video_fn = 'video.mp4',
        )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ENTRY
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == '__main__':

    main()
