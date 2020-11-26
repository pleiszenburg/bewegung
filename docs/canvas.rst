.. _drawing:

Drawing: Canvas Types & Backends
================================

``bewegung`` offers a set of "backends" for drawing on canvases. A specific canvas can be selected with the ``Video.canvas`` method. Full access to the inventory of backends and all of their functionality is provided through a ``backends`` dictionary.

Canvas Factories: ``Video.canvas``
----------------------------------

The ``Video.canvas`` method is typically used to configure a layer. It returns a "factory", i.e. a special function, which can be called to generate new pre-configured canvases of a certain type.

.. code:: python

    from bewegung import Video

    v = Video(width = 1920, height = 1080, seconds = 10.0)

    canvas_factory = v.canvas(backend = 'drawingboard')
    canvas_a = canvas_factory() # produce a new canvas
    canvas_b = canvas_factory() # produce a yet another new canvas

In the context of a layer's configuration, the use of ``Video.canvas`` looks as follows. Note that ``DrawingBoard`` is in fact the default canvas, so it usually does not have to be explicitly selected. A new, pre-configured canvas of the requested type is fed into the layer method for every individual video frame.

.. code:: python

    from bewegung import Video

    v = Video(width = 1920, height = 1080, seconds = 10.0)

    @v.sequence()
    class Foo:

        @v.layer(canvas = v.canvas(backend = 'drawingboard'))
        def bar(self, canvas): # a new canvas is generated and passed once per frame
            return canvas

Parameters of the ``Video.canvas`` method other than ``backend``, i.e. the name of the selected backend, are usually forwarded to the underlying library. However, the various backends of ``bewegung`` may fill certain parameters with reasonable defaults or fix inconsistencies that can be problematic in the context of generating videos. See chapters on individual backends below.

Inventory of ``backends``
-------------------------

All backends can be accessed via the ``backends`` dictionary, which represents the inventory of backends.

.. code:: ipython

    >>> from bewegung import backends
    >>> backends.keys()
    dict_keys(['drawingboard', 'pil', 'datashader', 'cairo', 'matplotlib'])
    >>> [backend for backend in backends.values()]
    [<DrawingBoardBackend>, <PillowBackend>, <DatashaderBackend>, <CairoBackend>, <MatplotlibBackend>]

Backends are "lazy" objects. They only import the underlying library if actually used. For most intents and purposes, working with ``Video.canvas`` is sufficient. Further details about the common structure of backends are provided in the :ref:`sections on custom backends <custombackends>`.

Backend: ``DrawingBoard``
-------------------------

Foo bar.

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
  :alt: Output

Similar to ``ImageSurface``, the function call ``v.canvas(backend = 'cairo')`` accepts the following additional keyword arguments:

- ``format``, by default ``cairo.FORMAT_ARGB32``. If a format other than ARGB32 is specified, the layer method is supposed to return a Pillow Image object instead of an ``ImageSurface`` object, i.e. in this case the conversion to Pillow's image format is left to the user. Alternatively, the user may also convert the non-ARGB32 ``ImageSurface`` object to an ARGB32 ``ImageSurface`` object before returning it.
- ``width``, width of the video by default
- ``height``, height of video by default

Backend: ``Pillow``
-------------------

Foo bar.

Backend: ``datashader``
-----------------------

Foo bar.

Backend: ``matplotlib``
-----------------------

Foo bar.

.. _acceleratingmatplotlib:

Accelerating ``matplotlib``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Foo bar.

.. _custombackends:

Defining & Registering Custom Backends
--------------------------------------

Foo bar.

Demo backend with numpy ...

Cross-Backend Abstraction: Colors
---------------------------------

Foo bar.
