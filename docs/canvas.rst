.. _drawing:

Drawing: Canvas Types & Backends
================================

``bewegung`` offers a set of "backends" for drawing on canvases. A specific backend can be selected and configured through the :meth:`bewegung.Video.canvas` method. Full access to the inventory of backends and all of their functionality is provided through the ``backends`` dictionary.

.. toctree::
   :maxdepth: 2
   :caption: The API in detail

   canvas_factories
   backends
   drawingboard
   pycairo
   pillow
   datashader
   matplotlib
   custom_backends
   colors
