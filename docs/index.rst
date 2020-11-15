a versatile video renderer

User's guide
============

``bewegung`` is a versatile video renderer, primarily targeting scientific visualizations of large quantities of data. Its core concepts are *sequences* and *layers*. Sequences describe a certain time span within a video and can overlap. Each sequence can hold multiple layers. Layers can be generated with ``cairo``, ``Pillow``, ``datashader`` and ``bewegung``'s internal drawing system ``DrawingBoard``. Final compositing of every video frame and video effects are implemented via `Pillow`. ``bewegung`` also includes a simple vector algebra system and a "camera" for 3D to 2D projections. ``bewegung`` is developed with ease of use, compute time and memory efficiency in mind.

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents

   installation
   getting_started
   time
   video
   algebra

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
