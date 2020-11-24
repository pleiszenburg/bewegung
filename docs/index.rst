``bewegung`` - a versatile video renderer

User's Guide
============

``bewegung`` is a versatile video renderer, primarily targeting scientific visualizations of large quantities of data. Its core concepts are *sequences* and *layers*. Sequences describe a certain time span within a video and can overlap. Each sequence can hold multiple layers. Layers can be generated with ``cairo``, ``Pillow``, ``datashader``, ``matplotlib`` and ``bewegung``'s internal drawing system ``DrawingBoard``. Final compositing of every video frame and video effects are implemented via ``Pillow``. Video encoding is handled by ``ffmpeg``. ``bewegung`` also includes a simple vector algebra system and a "camera" for 3D to 2D projections. ``bewegung`` is developed with ease of use, compute time and memory efficiency in mind.

Why another library for rendering / animating videos?
-----------------------------------------------------

Many plotting & visualization libraries from the scientific Python ecosystem, such as ``matplotlib`` for instance, have integrated animation functionality. Rendering individual frames as still images and streaming them to ``ffmpeg`` for video encoding is also a rather common practice. However, as soon as more than one plotting or visualization library becomes relevant within a single animation and/or the video is supposed to become more structured and/or the video rendering process needs to scale (parallelization, in other words), things become pretty messy rather quickly. This library is based on the experiences made while writing a fair number of custom animated visualization pipelines. It collects and abstracts all common bits and pieces and offers clean structures for typical tasks. At the time of writing, it is the third iteration on the idea of having such a library. The first two iterations were never published, but the lessons learned from the mistakes made in their development went into designing this very library. Welcome to ``bewegung``!

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents

   installation
   getting_started
   canvas
   video
   algebra
   debug

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
