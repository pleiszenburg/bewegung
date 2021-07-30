.. _custombackends:

Defining & Registering Custom Backends
======================================

``bewegung`` allows to add new, custom backends. It is a two-step process. First, a backend class must be derived from :class:`bewegung.BackendBase`. Second, an instance / object of this class must be added to the ``bewegung.backends`` dictionary.

The ``BackendBase`` API
-----------------------

Derive from this class when implementing a new backend.

.. autoclass:: bewegung.BackendBase
    :members:
    :private-members:

A Minimal Backend based on ``numpy``
------------------------------------

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
