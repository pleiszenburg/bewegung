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

``backends`` Inventory
----------------------

All backends can be accessed via the ``backends`` dictionary, which represents the inventory of backends.

.. code:: ipython

    >>> from bewegung import backends
    >>> backends.keys()
    dict_keys(['drawingboard', 'pil', 'datashader', 'cairo', 'matplotlib'])
    >>> [backend for backend in backends.values()]
    [<DrawingBoardCanvas>, <PillowCanvas>, <DatashaderCanvas>, <CairoCanvas>, <MatplotlibCanvas>]

Backends are "lazy" objects. They only import the underlying library if actually used. For most intends and purposes, working with ``Video.canvas`` is sufficient. Further details about the common structure of backends are provided in the :ref:`sections on custom backends <custombackends>`

Backend: ``DrawingBoard``
-------------------------

Foo bar.

Backend: ``pycairo``
--------------------

Foo bar.

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
