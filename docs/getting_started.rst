Getting Started
===============

``bewegung`` provides classes and functions for defining and rendering videos. Various drawing and plotting libraries can virtually transparently be integrated into this process. ``bewegung`` manages the composition of the video frames, in parallel if desired, and streams them to ``ffmpeg`` for video encoding.

Minimal Example
---------------

A video can be generated in three easy steps:

1. Creating a *video object*
2. Defining *sequences* and *layers* (via decorators)
3. *Rendering* the video

The following code snipped will create an empty, black video, 10 seconds long at 60 frames per second (fps) in `1080p`_:

.. code:: python

    from bewegung import Video

    # 1. create a video object
    v = Video(width = 1920, height = 1080, seconds = 10.0)

    # 2. define sequences
    @v.sequence()
    class Background:

        # ... and layers
        @v.layer()
        def empty(self, canvas):
            return canvas

    # 3. render the video
    v.render(video_fn = 'video.mp4')

.. _1080p: https://en.wikipedia.org/wiki/1080p

*Video objects* manage the subsequently defined components of a video. They can be understood as a thin data management structure combined with a simple scheduler. Every video can contain multiple (overlapping) *sequences*. Sequences are special, decorated classes. By default, a sequence is as long as its parent video - however, it can also be limited in length and begin at any desired time. A sequence can hold multiple *layers*. A layer is a special, decorated method within a sequence class that draws content onto a canvas and returns the "filled" canvas (i.e. the drawn image).

Complex Example
---------------

The following code snipped will create a 10 second long video at 30 fps in 1080p with a gray background and a red "ball" (filled circle) moving from the top left corner to the bottom right corner of the image:

.. code:: python

    from multiprocessing import cpu_count
    from bewegung import Video, Color, Vector2D, FadeInEffect, FadeOutEffect

    v = Video(width = 1920, height = 1080, frames = 300, fps = 30) # set output to 30 fps

    @v.sequence() # from start to finish of the video
    class Background:

        @v.layer(
            zindex = v.zindex.on_bottom(), # at the bottom of the stack
            canvas = v.canvas(background_color = Color(26, 26, 26)), # gray
        )
        def empty(self, canvas):
            return canvas # nothing to do, canvas remains empty

    @v.sequence(
        start = v.time_from_seconds(1.0), # start one second into the video
        stop = v.time_from_seconds(-1.0), # stop one second before end of video
    )
    class SomeForeground:

        @FadeInEffect(v.time_from_seconds(4.0)) # fade layer in for 4 seconds
        @FadeOutEffect(v.time_from_seconds(2.0)) # fade layer out for 2 seconds
        @v.layer(
            zindex = v.zindex.on_top(), # on top of the stack
            canvas = v.canvas(background_color = Color(26, 26, 26, 0)), # transparent gray
        )
        def moving_red_ball(self, canvas, reltime): # request relative time within sequence
            factor = reltime / self.length
            canvas.draw_filledcircle(
                point = Vector2D(factor * v.width, factor * v.height),
                r = 10,
                fill_color = Color(255, 0, 0),
                )
            return canvas

    v.render(video_fn = 'video.mp4', processes = cpu_count()) # render video frames in parallel

Compared to the initial minimal example, the above complex example contains two sequences with one layer each. The video, the layers and the sequences are a lot more configured. The video for instance is not defined based on its length in seconds. Instead, the number of frames is provided. Besides, the video is not using ``bewegung``'s default frame rate of 60 fps but 30 fps instead.

The "empty" layer in the "Background" sequence receives a background color, a dark gray tone. It is provided with an explicit z-index at the bottom of the stack of layers. The "SomeForeground" sequence begins 1 second into the video and ends one second before the end of the video. The "moving_red_ball" layer has a transparent background color so the "empty" layer from the "Background" sequence becomes visible. It is also provided with an explicit z-index - this time at the top of the stack of layers. In addition, the "moving_red_ball" layer is decorated with *video effects*, making it to fade in and out.

The video frames are *rendered in parallel*. The ``processes`` parameter of the ``Video.render`` method defines the number of parallel rendering processes. It is set to the `number of logical cores`_ of the computer's CPU(s). ``bewegung`` evaluates every layer once per video frame and composes all layers to an image - the actual video frame. Because of the parallel nature of ``bewegung``, the *generation of frames may occur out-of-order*. However, the video frames are always forwarded to the video encoder in order.

.. _number of logical cores: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.cpu_count

Prepare Tasks
-------------

In may be necessary to prepare or compute data prior to drawing onto a canvas. It may even be the case that multiple layers rely on the same data, which has to be prepared once per video frame. This is where *prepare tasks* become useful. They work very much like layers. There is a special decorator for indicating them. Prepare tasks can also be ordered in a system similar to the z-index of layers, the prepare-order (``preporder``). All prepare tasks are evaluated once per video frame and **before** the first layer is drawn.

.. code:: python

    from multiprocessing import cpu_count
    from bewegung import Video, Color, Vector2D

    v = Video(width = 1920, height = 1080, seconds = 10.0)

    @v.sequence()
    class Background:

        @v.layer(canvas = v.canvas(background_color = Color(26, 26, 26)))
        def empty(self, canvas):
            return canvas

    @v.sequence()
    class SomeForeground:

        def __init__(self):
            self._factor = None # initialize variable which will eventually hold the data

        @v.prepare(
            preporder = v.preporder.on_bottom(), # this prepare task comes firth in line ("bottom of stack")
        ) # prepare task decorator
        def compute_data(self, reltime): # prepare task method, requesting relative time within sequence
            self._factor = reltime / self.length # prepare data

        @v.layer(canvas = v.canvas(background_color = Color(26, 26, 26, 0)))
        def moving_red_ball(self, canvas): # only request canvas
            canvas.draw_filledcircle(
                point = Vector2D(self._factor * v.width, self._factor * v.height),
                r = 10,
                fill_color = Color(255, 0, 0),
                )
            return canvas

    v.render(video_fn = 'video.mp4', processes = cpu_count())

In the above example, a single prepare task is defined. It computes a "factor" which is eventually picked up by the "moving_red_ball" layer. The "SomeForeground" sequence class' constructor is used to initialize the "factor" variable.

Rendering Frames as Images instead of Videos
--------------------------------------------

For debugging and development, it can be very useful to be able to selectively render individual frames into image files or interactively work with the resulting image objects.

.. code:: python

    from bewegung import Video

    v = Video(width = 1920, height = 1080, seconds = 10.0)

    @v.sequence()
    class Background:

        @v.layer()
        def empty(self, canvas):
            return canvas

    v.reset() # reset video object before frames can be saved!
    v.render_frame(
        time = v.time(45), # frame number 45
        frame_fn = 'some_frame.png', # save to location as PNG
        )
    pillow_image_object = v.render_frame(
        time = v.time_from_seconds(1.0), # frame at 1 second
        ) # returns a Pillow.Image object

Instead of calling ``Video.render``, the video object can be manually *reset* by calling ``Video.reset``. A reset is usually taken care of by the video render method, but if individual frames are desired instead, it has to be called at least once before the first video frame is generated. Once this is done, frames can be selected based on their time and rendered with ``Video.render_frame``. This method can both directly store the frame into a file and return it as a ``Pillow.Image`` object, see `Pillow documentation`_.

.. _Pillow documentation: https://pillow.readthedocs.io/en/stable/reference/Image.html#the-image-class

Using & Mixing Backends
-----------------------

Foo bar.

Requesting Parameters in Layers and Prepare Tasks
-------------------------------------------------

Foo bar.

Working with Time
-----------------

Time, TimeScale ...

Convenience Functionality
-------------------------

Vectors, Camera, Color
