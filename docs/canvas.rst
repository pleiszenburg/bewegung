.. _drawing:

Drawing: Canvas Types & Backends
================================

``bewegung`` offers a set of "backends" for drawing on canvases. A specific backend can be selected and configured through the ``Video.canvas`` method. Full access to the inventory of backends and all of their functionality is provided through the ``backends`` dictionary.

Canvas Factories: ``Video.canvas``
----------------------------------

The ``Video.canvas`` method is typically used to configure a layer. It returns a "factory", i.e. a special function, which can be called to generate new pre-configured canvases of a certain type.

.. code:: python

    from bewegung import Video

    v = Video(width = 1920, height = 1080, seconds = 10.0)

    canvas_factory = v.canvas(backend = 'drawingboard')
    canvas_a = canvas_factory() # produce a new canvas
    canvas_b = canvas_factory() # produce yet another new canvas

In the context of a layer's configuration, the use of ``Video.canvas`` looks as follows.

.. note::

    ``DrawingBoard`` is the default backend, so it usually does not have to be explicitly selected.

A new, pre-configured canvas of the requested type is fed into the layer method for every individual video frame.

.. code:: python

    from bewegung import Video

    v = Video(width = 1920, height = 1080, seconds = 10.0)

    @v.sequence()
    class Foo:

        @v.layer(canvas = v.canvas(backend = 'drawingboard'))
        def bar(self, canvas): # a new canvas is generated and passed once per frame
            return canvas

Parameters of the ``Video.canvas`` method other than ``backend``, i.e. the name of the selected backend, are usually forwarded to the underlying library.

.. warning::

    The various backends of ``bewegung`` may fill certain parameters of their underlying libraries with reasonable defaults or fix inconsistencies that can be problematic in the context of generating videos. See chapters on individual backends below.

Inventory of ``backends``
-------------------------

All backends can be accessed via the ``backends`` dictionary, which represents the inventory of backends.

.. code:: ipython

    >>> from bewegung import backends
    >>> backends.keys()
    dict_keys(['drawingboard', 'pillow', 'datashader', 'cairo', 'matplotlib'])
    >>> [backend for backend in backends.values()]
    [<DrawingBoardBackend>, <PillowBackend>, <DatashaderBackend>, <CairoBackend>, <MatplotlibBackend>]

Backends are "lazy" objects. They only import the underlying library if actually used. For most intents and purposes, working with ``Video.canvas`` is sufficient. Further details about the common structure of backends are provided in the :ref:`sections on custom backends <custombackends>`.

.. _drawingboard:

Backend: ``DrawingBoard``
-------------------------

The ``DrawingBoard`` backend provides relatively easy facilities for drawing lines, circles, other geometric primitives, text and SVGs. It is not meant for complex drawings or performance. A detailed :ref:`description of its API <drawingboardapi>` is provided below. ``DrawingBoard`` is essentially a wrapper around ``cairo``, ``Pango`` and ``rsvg``. Besides, ``bewegung`` also offers an explicit :ref:`cairo backend <backendcairo>`. If no backend is specified, layers will typically fall back to ``DrawingBoard``. A simple example using ``DrawingBoard`` looks as follows:

.. code:: python

    from bewegung import Video, Vector2D, Color

    v = Video(width = 480, height = 270, seconds = 1.0)

    @v.sequence()
    class Foo:

        @v.layer(canvas = v.canvas(backend = 'drawingboard'))
        def bar(self, canvas): # a DrawingBoard object

            canvas.draw_polygon(
                Vector2D(5, 5), Vector2D(v.width - 5, v.height - 5),
                line_width = 3,
                line_color = Color(255, 0, 0, 255),
            )

            return canvas

    v.reset()
    v.render_frame(v.time(0))

.. image:: _static/backend_drawingboard.png
  :width: 480
  :alt: DrawingBoard output

The function call ``v.canvas(backend = 'drawingboard')`` accepts additional keyword arguments, which are passed on to the :ref:`DrawingBoard constructor <drawingboardapi>`. By default, the canvas size is set to the width and height of the video.

.. _drawingboardapi:

The ``DrawingBoard`` Class
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``DrawingBoard`` class makes use of :ref:`vectors <vectors>` and :ref:`colors <colors>`.

.. autoclass:: bewegung.core.backends.drawingboard.core.DrawingBoard
    :members:
    :private-members:

.. note::

    The ``DrawingBoard`` class can, most efficiently, be accessed via ``bewegung.backends['drawingboard'].type``.

.. _backendcairo:

Backend: ``pycairo``
--------------------

The ``pycairo`` backend allows to generate pre-configured ``ImageSurface`` objects, see `pycairo documentation`_.

.. _pycairo documentation: https://pycairo.readthedocs.io/en/latest/reference/surfaces.html?highlight=ImageSurface#cairo.ImageSurface

.. code:: python

    import cairo
    from bewegung import Video

    v = Video(width = 480, height = 270, seconds = 1.0)

    @v.sequence()
    class Foo:

        @v.layer(canvas = v.canvas(backend = 'cairo'))
        def bar(self, canvas): # a pyrairo ImageSurface, mode ARGB32

            ctx = cairo.Context(canvas)

            ctx.move_to(5, 5)
            ctx.line_to(v.width - 5, v.height - 5)
            ctx.set_source_rgba(1, 0, 0, 1)
            ctx.set_line_width(3)
            ctx.stroke()

            return canvas

    v.reset()
    v.render_frame(v.time(0))

.. image:: _static/backend_cairo.png
  :width: 480
  :alt: Cairo output

Similar to ``cairo.ImageSurface``, the function call ``v.canvas(backend = 'cairo')`` accepts the following additional keyword arguments:

- ``format``, by default ``cairo.FORMAT_ARGB32``. If a format other than ARGB32 is specified, the layer method is supposed to return a Pillow Image object of mode ``'RGBA'`` instead of an ``ImageSurface`` object, i.e. in this case the conversion to Pillow's image format is left to the user. Alternatively, the user may also convert the non-ARGB32 ``ImageSurface`` object to an ARGB32 ``ImageSurface`` object before returning it from the layer method.
- ``width``, width of the video by default
- ``height``, height of the video by default

Backend: ``Pillow``
-------------------

Because ``bewegung`` is literally built around ``Pillow``, the ``Pillow`` backend is by far the most simple one in the collection. For further details, please consult the `documentation of Pillow`_.

.. _documentation of Pillow: https://pillow.readthedocs.io

.. code:: python

    from PIL import ImageDraw
    from bewegung import Video

    v = Video(width = 480, height = 270, seconds = 1.0)

    @v.sequence()
    class Foo:

        @v.layer(canvas = v.canvas(backend = 'pillow'))
        def bar(self, canvas): # a Pillow Image, mode RGBA

            draw = ImageDraw.Draw(canvas)
            draw.line(
                ((5, 5), (v.width - 5, v.height - 5)),
                fill = (255, 0, 0, 255), width = 3,
            )

            return canvas

    v.reset()
    v.render_frame(v.time(0))

.. image:: _static/backend_pillow.png
  :width: 480
  :alt: Pillow output

Similar to ``PIL.Image.new``, the function call ``v.canvas(backend = 'pillow')`` accepts the following additional keyword arguments:

- ``mode``, by default ``'RGBA'``. If a format other than ``'RGBA'`` is specified, the user has to convert the Image to ``'RGBA'`` before returning it from the layer method.
- ``size``, a tuple of width and height. Width and height of the video by default.
- ``color``, a background color. Uses ``Pillow``'s default, black.
- ``width``, mapped to ``size`` if provided together with ``height``.
- ``height``, mapped to ``size`` if provided together with ``width``.
- ``background_color``, mapped to ``color``. Accepts ``bewegung.Color`` objects.

.. _datashader:

Backend: ``datashader``
-----------------------

The ``datashader`` package is a high-performance graphics pipeline for visualizing very large quantities of data. For further details, please consult the `documentation of datashader`_.

.. _documentation of datashader: https://datashader.org/

.. code:: python

    import numpy as np
    import pandas as pd
    import datashader.transfer_functions as tf
    from bewegung import Video

    v = Video(width = 480, height = 270, seconds = 1.0)

    @v.sequence()
    class Foo:

        @v.layer(
            canvas = v.canvas(
                backend = 'datashader',
                x_range = (-9.6, 9.6),
                y_range = (-5.4, 5.4),
            )
        )
        def bar(self, canvas): # a datashader canvas object

            points = 100000
            df = pd.DataFrame(dict(
                x = np.random.normal(size = points),
                y = np.random.normal(size = points),
            ))

            agg = canvas.points(df, 'x', 'y')
            img = tf.shade(agg, cmap = ['lightblue', 'darkblue'], how = 'log')

            return img # a datashader.transfer_functions.Image object

    v.reset()
    v.render_frame(v.time(0))

.. image:: _static/backend_datashader.png
  :width: 480
  :alt: Datashader output

Similar to ``datashader.Canvas``, the function call ``v.canvas(backend = 'datashader')`` accepts the following additional keyword arguments:

- ``plot_width``, width of the video by default
- ``plot_height``, height of the video by default
- ``x_range``, by default ``None``
- ``y_range``, by default ``None``
- ``x_axis_type``, by default ``'linear'``
- ``y_axis_type``, by default ``'linear'``
- ``width``, mapped to ``plot_width``
- ``height``, mapped to ``plot_height``

Layer methods are expected to return ``datashader.transfer_functions.Image`` objects or, alternatively, Pillow Image objects.

.. warning::

    If a ``datashader.transfer_functions.Image`` object is returned, ``bewegung`` will mirror the image along the x-axis, i.e. the y-axis will be flipped. This makes the output consistent with ``Pillow`` and ``pycairo``, were the y-axes is positive downwards. The flip can be avoided by manually converting the image to a Pillow Image object before returning, i.e. ``return img.as_pil()`` in the above example.

Backend: ``matplotlib``
-----------------------

The ``matplotlib`` library is a - if not the - classic plotting package in the Python ecosystem. For further details, please consult the `documentation of matplotlib`_. A good basic introduction can also be found in the `Python Data Science Handbook`_ (2016), chapter 4, by `Jake VanderPlas`_. The author has made the `manuscript freely available in the form of Jupyter notebooks on Github`_.

.. _documentation of matplotlib: https://matplotlib.org/contents.html
.. _Python Data Science Handbook: https://www.worldcat.org/search?q=isbn:9781491912058
.. _Jake VanderPlas: https://twitter.com/jakevdp
.. _manuscript freely available in the form of Jupyter notebooks on Github: https://github.com/jakevdp/PythonDataScienceHandbook

.. code:: python

    from bewegung import Video

    v = Video(width = 480, height = 270, seconds = 1.0)

    @v.sequence()
    class Foo:

        @v.layer(
            canvas = v.canvas(
                backend = 'matplotlib',
                facecolor = '#FFFFFFFF',
                dpi = 150,
            )
        )
        def bar(self, canvas): # a matplotlib figure object

            ax = canvas.subplots()
            ax.plot([1, 2, 3], [5, 4, 7])

            return canvas

    v.reset()
    v.render_frame(v.time(0))

.. image:: _static/backend_matplotlib.png
  :width: 480
  :alt: Matplotlib output

Similar to ``matplotlib.pyplot.figure``, the function call ``v.canvas(backend = 'matplotlib')`` accepts the following additional keyword arguments, among others (see documentation of `matplotlib.pyplot.figure`_ and `matplotlib.figure.Figure`_):

.. _matplotlib.pyplot.figure: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.figure.html#matplotlib.pyplot.figure
.. _matplotlib.figure.Figure: https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure

- ``dpi``, resolution or *dots per inch*. 300 by default.
- ``figsize``, a tuple of width and height *in inches*. Width and height of the video by default, converted to inches based on the value of ``dpi``.
- ``width``, width *in pixels*. Mapped to ``figsize`` if provided together with ``height``. Converted to inches based on the value of ``dpi``.
- ``height``, height *in pixels*. Mapped to ``figsize`` if provided together with ``width``. Converted to inches based on the value of ``dpi``.
- ``tight_layout``, by default ``True``.
- ``facecolor``, a background color.
- ``background_color``, mapped to ``facecolor``. Accepts ``bewegung.Color`` objects.
- ``managed``, a boolean, by default ``True``. This value indicates whether the the ``matplotlib.figure.Figure`` object is "managed" by ``bewegung``. If ``True``, ``bewegung`` will close, i.e. destroy, a figure that is returned by a layer method.

Layer methods are expected to return ``matplotlib.figure.Figure`` objects.

.. warning::

    By default, ``bewegung`` will "manage" ``matplotlib.figure.Figure`` objects for saving resources, i.e. the returned ``matplotlib.figure.Figure`` objects are automatically closed once returned. This can be avoided by setting ``managed`` to ``False``.

.. _acceleratingmatplotlib:

Accelerating ``matplotlib``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aside from its rich set of features, ``matplotlib`` is known for its mediocre performance. Not to be confused with ``bewegung``'s backends, ``matplotlib`` also has `different backends for rendering`_. Within ``bewegung``, ``matplotlib`` is automatically configured to use `mplcairo`_, "A (new) cairo backend for Matplotlib". Compared to ``matplotlib``'s own built-in backends, its output quality is significantly better while the rendering speed is also higher. Unfortunately, ``mplcairo`` is just "half" of the story of ``matplotlib`` performance.

.. _mplcairo: https://github.com/matplotlib/mplcairo
.. _different backends for rendering: https://matplotlib.org/faq/usage_faq.html#what-is-a-backend

In animation frameworks for ``matplotlib``, such as the "official" `matplotlib.animation`_ sub-package, it is common practice to re-use and update existing figure and subplot / axes objects. This speeds up the rendering process considerably. This strategy is also supported by ``bewegung``.

.. warning::

    For optimal results, the suggested approach requires some deeper understanding of ``matplotlib``'s facilities.

The following code illustrates the approach.

.. _matplotlib.animation: https://matplotlib.org/api/animation_api.html

.. code:: python

    from bewegung import Video

    v = Video(width = 480, height = 270, seconds = 1.0)

    @v.sequence()
    class Foo:

        def __init__(self):

            self._fig = v.canvas(
                backend = 'matplotlib',
                facecolor = '#FFFFFFFF',
                dpi = 150,
                managed = False, # ensure that bewegung does not close figure
            )() # calls the factory once, generates a single figure
            self._ax = self._fig.subplots() # generates a single subplot

        @v.layer() # no backend configuration required
        def bar(self): # no canvas requested

            self._ax.clear() # optional: update content directly instead
            self._ax.plot([1, 2, 3], [5, 4, 7]) # draw new content or change old content

            return self._fig

    v.reset()
    image0 = v.render_frame(v.time(0))
    image1 = v.render_frame(v.time(1))

The less a figure changes, the faster the above code becomes. Depending on the degree of complexity and optimization, anything from a few percent to an order of magnitude of performance gain can be achieved.

.. _custombackends:

Defining & Registering Custom Backends
--------------------------------------

``bewegung`` allows to add new, custom backends. It is a two-step process. First, a backend class must be derived from ``bewegung.BackendBase``. Second, an instance / object of this class must be added to the ``bewegung.backends`` dictionary.

The ``BackendBase`` API
~~~~~~~~~~~~~~~~~~~~~~~

Derive from this class when implementing a new backend.

.. autoclass:: bewegung.BackendBase
    :members:
    :private-members:

A Minimal Backend based on ``numpy``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example illustrates how to build a custom backend around the ``numpy`` library. ``numpy.ndarray`` objects are used as a canvas.

.. code:: python

    from typing import Any, Callable
    from PIL.Image import Image, fromarray
    from bewegung import (
        Video,
        BackendBase,
        backends,
    )

    class NumpyBackend(BackendBase):

        def __init__(self):

            super().__init__() # call BackendBase constructor!
            self._np = None # lazy import of numpy

        def _prototype(self, video: Video, **kwargs) -> Callable:

            width = kwargs.get('width', video.width)
            height = kwargs.get('height', video.height)

            def factory():
                canvas = self._np.zeros(
                    (width, height, 4),
                    dtype = 'u1', # uint8
                ) # black canvas, RGBA
                canvas[:, :, 3] = 255 # opaque
                return canvas

            return factory

        def _load(self):

            import numpy as np # lazy import of numpy
            self._np = np # lazy import of numpy

            self._type = np.ndarray # set type so it can be recognized

        def _to_pil(self, obj: Any) -> Image:

            if obj.dtype != self._np.uint8:
                raise TypeError('unhandled datatype')
            if obj.ndim != 3:
                raise TypeError('unhandled color configuration')
            if obj.shape[2] != 4:
                raise TypeError('unhandled color configuration')

            return fromarray(obj, mode = 'RGBA') # convert to Pillow Image and return

    backends['numpy'] = NumpyBackend() # register backend

    v = Video(width = 480, height = 270, seconds = 1.0)

    @v.sequence()
    class Foo:

        @v.layer(canvas = v.canvas(backend = 'numpy'))
        def bar(self, canvas): # a numpy ndarray

            canvas[30:50, 40:60, 0] = 255 # red square

            return canvas

    v.reset()
    v.render_frame(v.time(0))

.. image:: _static/backend_numpy.png
  :width: 480
  :alt: Numpy output

The ``_prototype`` method should return a factory function without parameters. It also processes keyword arguments, fixes them if required and sets defaults. The ``_load`` method is responsible for "lazy" loading of the underlying library, ``numpy`` in this case. The eventually returned canvas datatype must be assigned to ``_type``. The ``_to_pil`` method is responsible for converting the backend's canvas type to a Pillow Image object. It may also perform consistency checks.

.. _colors:

Cross-Backend Abstraction: Colors
---------------------------------

All backends work with variations of RGB, RGBA or RGBa color spaces. Some use pre-multiplied alpha values, some do not. Some accept RGB values as floats from 0.0 to 1.0, some accept RGB values as integers from 0 to 255, some expect hexadecimal notations as strings. The ``Color`` class tries to provide a common base for working with RGB(A) colors in different notations.

The ``Color`` API
~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.Color
    :members:
