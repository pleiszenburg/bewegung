About ``bewegung``
==================

Synopsis
--------

``bewegung`` is a versatile video renderer, primarily targeting scientific visualizations of large quantities of data. Its core concepts are *sequences* and *layers*. Sequences describe a certain time span within a video and can overlap. Each sequence can hold multiple layers. Layers can be generated with ``cairo`` (see `pycairo documentation`_), ``Pillow``/``PIL`` (see `Pillow documentation`_), ``datashader`` (see `datashader documentation`_), ``matplotlib`` (see `matplotlib documentation`_) and ``bewegung``'s internal drawing system ``DrawingBoard`` (see :ref:`chapter on drawing <drawing>`). Final compositing of every video frame and video effects are implemented via ``Pillow``. Video encoding is handled by ``ffmpeg`` (see `ffmpeg documentation`_). ``bewegung`` also includes a simple vector algebra system and a "camera" for 3D to 2D projections. ``bewegung`` is developed with ease of use, compute time and memory efficiency in mind.

.. _pycairo documentation: https://pycairo.readthedocs.io
.. _Pillow documentation: https://pillow.readthedocs.io
.. _datashader documentation: https://datashader.org/
.. _matplotlib documentation: https://matplotlib.org/contents.html
.. _ffmpeg documentation: https://ffmpeg.org/documentation.html

Why another library for rendering / animating videos?
-----------------------------------------------------

Many plotting & visualization libraries from the scientific Python ecosystem, such as ``matplotlib`` for instance, have integrated animation functionality. Rendering individual frames as still images and streaming them to ``ffmpeg`` for video encoding is also a rather common practice. However, as soon as more than one plotting or visualization library becomes relevant within a single animation and/or the video is supposed to become more structured and/or the video rendering process needs to scale (parallelization, in other words), things become pretty messy rather quickly. This library is based on the experiences made while writing a fair number of custom animated visualization pipelines. It collects and abstracts all common bits and pieces and offers clean structures for typical tasks. At the time of writing, it is the third iteration on the idea of having such a library. The first two iterations were never published, but the lessons learned from the mistakes made in their development went into designing this very library. Welcome to ``bewegung``!

Similar & Alternative Libraries
-------------------------------

There are various libraries in the overall Python ecosystem which target tasks related to animations and videos. Compared to ``bewegung``, they all serve more or less different use-cases and applications. It can even make a lot of sense to combine them with ``bewegung``.

- `MoviePy`_: An advanced (non-linear) video editing library with support for audio tracks. In theory, ``MoviePy`` can do a lot of what ``bewegung`` can do. However, in direct comparison, ``MoviePy``'s  main focus is on editing. While it is extremely good at that, building complicated multi-layer animations similar to ``bewegung`` becomes a rather tedious and unmaintainable task above a level of complexity. Where ``bewegung`` has mechanisms to generalize the integration of 3rd-party drawing and plotting libraries, ``MoviePy`` requires the user to write a lot of boilerplate code himself. ``MoviePy`` loads a lot of work off to ``ffmpeg``, but its own code can not (easily) be parallelized. ``bewegung`` is based on a fully parallelized implementation.
- `matplotlib.animation`_: As sub-package of ``matplotlib``, it focuses entirely on ``matplotlib``. It can do both interactive animations and videos. It allows to encode videos with ``ffmpeg`` but also integrates other encoders. In comparison to ``bewegung``, this framework is really primarily built around ``matplotlib``, its strengths and its quirks. While ``bewegung`` has a fully parallelized implementation, it is virtually impossible to parallelize ``matplotlib.animation``.
- `animatplot`_: Focuses on interactive animations virtually exclusively based on ``matplotlib``.
- `celluloid`_: A simple, thin wrapper around ``matplotlib`` for rendering videos.
- `plotly`_: The ``plotly`` library has deeply integrated functionality for interactive animations and dashboards. Its undisputed strength is `WebGL`_-based graphic acceleration. ``plotly`` is lacking any kind of functionality for rendering videos as well as rendering frames in parallel, while functionality of this kind could certainly be built around ``plotly``.
- `manim`_: The ``manim`` package provides excellent functionality for generating explanatory math videos. It can handle LaTeX expressions and animate all sorts of mathematical expressions and transformations. Similar to ``bewegung``, it also integrates its own ``cairo``-based drawing system and encodes videos with ``ffmpeg``. In direct comparison to ``bewegung``, ``manim`` serves a completely different but also very interesting use-case.
- `mayavi`_: The ``mayavi`` library has `excellent integrated features`_ for generating interactive, near-real-time 3D visualizations. It is fairly easy to use and provides graphics acceleration. It lacks built-in capabilities for generating videos.
- `vispy`_: The ``vispy`` package is the undisputed crown jewel of real-time visualization of large quantities of data with Python. Its great performance comes at a price, however: The user has to write `OpenGL shaders`_ in C++, which is anything but trivial. ``vispy`` does not have built-in features for video export.
- `glumpy`_: Very similar to ``vispy``, with even lower-level access to APIs and internal facilities. ``glumpy`` can export videos via ``ffmpeg`` and borrows code from ``MoviePy`` for this task.
- `ffmpeg-python`_: The ``ffmpeg-python`` package is an object-oriented Python wrapper around the ``ffmpeg`` command line tool. It is an extremely powerful tool on its own, making the otherwise complicated and error-prone specification of ``ffmpeg`` options relatively easy. ``bewegung`` offers its own thin wrapper around ``ffmpeg``, which can be substituted by ``ffmpeg-python`` if desired.
- `PyAV`_: Python bindings to the libraries underneath ``ffmpeg``. In a nutshell even far more complicated to use than the ``ffmpeg`` command line version.
- `blender`_: A list of Python tools for animations would not be complete without ``Blender``. Although ``Blender`` is a GUI application, it is fully programmable & controllable through Python. ``Blender``'s features far exceed those of ``bewegung``. It can be argued that ``Blender`` serves different use-cases, primarily 3D modeling, lighting and video editing, while it can certainly also do what ``bewegung`` does - just different and slightly more complicated.
- `QGIS`_: For GIS-related tasks, ``QGIS`` offers the `Temporal Controller`_ infrastructure. It can produce both interactive animations and videos. It can be programmed & controlled via Python.

.. _MoviePy: https://zulko.github.io/moviepy/
.. _matplotlib.animation: https://matplotlib.org/api/animation_api.html
.. _animatplot: https://animatplot.readthedocs.io/en/stable/
.. _celluloid: https://github.com/jwkvam/celluloid
.. _plotly: https://plotly.com/python/animations/
.. _WebGL: https://en.wikipedia.org/wiki/WebGL
.. _manim: https://github.com/3b1b/manim
.. _mayavi: https://docs.enthought.com/mayavi/mayavi/index.html
.. _excellent integrated features: https://docs.enthought.com/mayavi/mayavi/mlab_animating.html
.. _vispy: https://vispy.org/
.. _glumpy: https://github.com/glumpy/glumpy
.. _OpenGL shaders: https://www.khronos.org/opengl/wiki/Shader
.. _ffmpeg-python: https://github.com/kkroening/ffmpeg-python
.. _PyAV: https://github.com/PyAV-Org/PyAV
.. _blender: https://www.blender.org/
.. _QGIS: https://www.qgis.org/
.. _Temporal Controller: https://anitagraser.com/2020/05/10/timemanager-is-dead-long-live-the-temporal-controller/
