Installation
============

Quick Install Guide
-------------------

``bewegung`` can be installed with Python's package manager ``pip``:

.. code:: bash

    pip install -vU bewegung

``bewegung`` has only one "hard" Python dependency, `the Pillow library`_.

.. _the Pillow library: https://pillow.readthedocs.io

All further Python dependencies are optional and allow to use certain optional components of ``bewegung``. A complete installation of all Python components and development tools can be triggered by running:

.. code:: bash

    pip install -vU bewegung[all]

Certain **non-Python components must installed separately and before invoking the above command**. For further instructions, see below. Most notably, ``ffmpeg`` should be installed for producing actual video files instead of video frames as individual files.

In principle, ``bewegung`` works across all modern operating systems. In terms of memory usage and performance, it behaves best on Unix-like systems due to `Windows's lack of "fork"`_.

.. _Windows's lack of "fork": https://stackoverflow.com/q/985281/1672565

Detailed Installation Options
-----------------------------

**For rendering an actual video** file, ``ffmpeg`` is required. See `download section`_ on ``ffmpeg``'s project website for installation instructions. If ``ffmpeg`` is not present, individual video frames can still be exported as image files.

.. _download section: https://ffmpeg.org/download.html

For a nice **progress bar** during video rendering (``pip install -vU bewegung[tqdm]``):

- ``tqdm`` (optional dependency)

For the **drawingboard rendering backend** (optional component, ``pip install -vU bewegung[drawingboard]``):

- ``pycairo``
- ``PyGObject``
- ``ipython`` (optional dependency, ``pip install -vU bewegung[ipython]``)

The `cairo library`_ and its headers must be installed, see `pycairo's documentation`_. The `prerequisites of PyQObject`_ must be fulfilled before installing it. In addition, `Pango`_, its headers (development package), `librsvg`_ and its headers (development package) must be all be present. ``drawingboard`` works without `ipython`_ if no interactive display of images in `Jupyter`_ is required.

.. _prerequisites of PyQObject: https://pygobject.readthedocs.io/en/latest/getting_started.html
.. _Pango: https://pango.gnome.org/
.. _librsvg: https://wiki.gnome.org/Projects/LibRsvg
.. _ipython: https://ipython.org/
.. _Jupyter: https://jupyter.org/

For the **cairo rendering backend** (optional component, ``pip install -vU bewegung[cairo]``):

- ``pycairo``

The `cairo library`_ and its headers must be installed, see `pycairo's documentation`_.

.. _cairo library: https://www.cairographics.org/
.. _pycairo's documentation: https://pycairo.readthedocs.io/en/latest/getting_started.html

For the **datashader rendering backend** (optional component, ``pip install -vU bewegung[datashader]``):

- ``datashader``

For further instructions, see `datashader's documentation`_.

.. _datashader's documentation: https://datashader.org/getting_started/index.html

For the **matplotlib rendering backend** (optional component, ``pip install -vU bewegung[matplotlib]``):

- ``numpy``
- ``matploblib``
- ``pycairo``
- ``mplcairo``

The `cairo library`_ and its headers must be installed, see `pycairo's documentation`_.

For a **faster camera** based Just-in-Time (JIT) compilation (``pip install -vU bewegung[numba]``):

- ``numba``

For further instructions, see `numba's documentation`_.

.. _numba's documentation: https://numba.readthedocs.io/en/stable/user/installing.html

For **vector arrays** and a **faster camera** based on ``numpy``'s array types (``pip install -vU bewegung[numpy]``):

- ``numpy``

For **run-time type-checking** across the library (see :ref:`debugging <debug>`):

- ``typeguard``
