Installation
============

Quick Install Guide
-------------------

``bewegung`` can be installed with Python's package manager ``pip``:

.. code:: bash

    pip install -vU bewegung

``bewegung`` has only one "hard" Python dependency, `the Pillow library`_.

.. _the Pillow library: https://pillow.readthedocs.io

All further Python dependencies are optional and allow to use certain optional components of ``bewegung``. A **complete installation** of all Python components and development tools can be triggered by running:

.. code:: bash

    pip install -vU bewegung[all]

.. warning::

    Certain **non-Python components must installed separately and before invoking the above command**. For further instructions, see :ref:`detailed installation instructions <detailedinstallation>`. Most notably, ``ffmpeg`` should be installed for producing actual video files instead of video frames as individual files.

In principle, ``bewegung`` works across all modern operating systems.

.. note::

    In terms of memory usage and performance, ``bewegung`` behaves best on Unix-like systems due to `Windows's lack of "fork"`_.

.. _Windows's lack of "fork": https://stackoverflow.com/q/985281/1672565

.. _detailedinstallation:

Detailed Installation Options
-----------------------------

Video File Encoding
~~~~~~~~~~~~~~~~~~~

For rendering an actual video file, ``ffmpeg`` is required. See `download section`_ on ``ffmpeg``'s project website for installation instructions. If ``ffmpeg`` is not present, individual video frames can still be exported as image files.

.. _download section: https://ffmpeg.org/download.html

Progress Bars
~~~~~~~~~~~~~

Installation: ``pip install -vU bewegung[tqdm]``

Dependencies:

- ``tqdm``

Drawingboard Rendering Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installation: ``pip install -vU bewegung[drawingboard]``

Dependencies:

- ``pycairo``
- ``PyGObject``
- ``ipython`` (optional dependency, ``pip install -vU bewegung[ipython]``)

The `cairo library`_ and its headers must be installed, see `pycairo's documentation`_. The `prerequisites of PyQObject`_ must be fulfilled before installing it. In addition, `Pango`_, its headers (development package), `librsvg`_ and its headers (development package) must be all be present. ``drawingboard`` works without `ipython`_ if no interactive display of images in `Jupyter`_ is required.

.. _prerequisites of PyQObject: https://pygobject.readthedocs.io/en/latest/getting_started.html
.. _Pango: https://pango.gnome.org/
.. _librsvg: https://wiki.gnome.org/Projects/LibRsvg
.. _ipython: https://ipython.org/
.. _Jupyter: https://jupyter.org/

Cairo Rendering Backend
~~~~~~~~~~~~~~~~~~~~~~~

Installation: ``pip install -vU bewegung[cairo]``

Dependencies:

- ``pycairo``

The `cairo library`_ and its headers must be installed, see `pycairo's documentation`_.

.. _cairo library: https://www.cairographics.org/
.. _pycairo's documentation: https://pycairo.readthedocs.io/en/latest/getting_started.html

Datashader Rendering Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installation: ``pip install -vU bewegung[datashader]``

Dependencies:

- ``datashader``

For further instructions, see `datashader's documentation`_.

.. _datashader's documentation: https://datashader.org/getting_started/index.html

Matplotlib Rendering Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installation: ``pip install -vU bewegung[matplotlib]``

Dependencies:

- ``numpy``
- ``matploblib``
- ``pycairo``
- ``mplcairo``

The `cairo library`_ and its headers must be installed, see `pycairo's documentation`_.

Faster Camera
~~~~~~~~~~~~~

Installation: ``pip install -vU bewegung[numba]``

Dependencies:

- ``numba`` for Just-in-Time (JIT) compilation

For further instructions, see `numba's documentation`_.

.. _numba's documentation: https://numba.readthedocs.io/en/stable/user/installing.html

Vector Arrays and Faster Camera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installation: ``pip install -vU bewegung[numpy]``

Dependencies:

- ``numpy``

Run-Time Type-Checking
~~~~~~~~~~~~~~~~~~~~~~

Installation: ``pip install -vU bewegung[typeguard]``

- ``typeguard``

If installed, type-checking will be enabled across the library (see :ref:`debugging <debug>`).
