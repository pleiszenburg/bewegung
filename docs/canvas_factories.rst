Canvas Factories: ``Video.canvas``
==================================

The :meth:`bewegung.Video.canvas` method is typically used to configure a layer. It returns a "factory", i.e. a special function, which can be called to generate new pre-configured canvases of a certain type.

.. code:: python

    from bewegung import Video

    v = Video(width = 1920, height = 1080, seconds = 10.0)

    canvas_factory = v.canvas(backend = 'drawingboard')
    canvas_a = canvas_factory() # produce a new canvas
    canvas_b = canvas_factory() # produce yet another new canvas

In the context of a layer's configuration, the use of :meth:`bewegung.Video.canvas` looks as follows.

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

Parameters of the :meth:`bewegung.Video.canvas` method other than ``backend``, i.e. the name of the selected backend, are usually forwarded to the underlying library.

.. warning::

    The various backends of ``bewegung`` may fill certain parameters of their underlying libraries with reasonable defaults or fix inconsistencies that can be problematic in the context of generating videos. See chapters on individual backends below.
