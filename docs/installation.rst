Installation
============

System Requirements
-------------------

In principle, ``bewegung`` works across all modern operating systems. ``bewegung`` is fully parallelized, so it significantly benefits from higher numbers of cores. Its memory consumption hugely depends on the complexity of the project. For example, ``bewegung``'s relatively simple `standard demo`_ requires at least 2 GBytes of RAM on a headless server or 4 GBytes of RAM on a desktop. Swapping is generally a bad idea - swap should be completely deactivated if possible.

.. note::

    In terms of memory usage and performance, ``bewegung`` behaves best on Unix-like systems due to `Windows's lack of "fork"`_.

.. _Windows's lack of "fork": https://stackoverflow.com/q/985281/1672565

Quick Install Guide
-------------------

`bewegung` can be installed both via ``conda`` and via ``pip``.

Via ``conda``
~~~~~~~~~~~~~

An almost complete installation can be triggered by running:

.. code:: bash

    conda install -c conda-forge bewegung

.. note::

    `mplcairo`_, a dependency of ``bewegung`` and alternative backend for ``matplotlib``, is currently not available via ``conda`` and must be installed manually. ``bewegung`` :ref:`does also work without mplcairo present <acceleratingmatplotlib>` and falls back to the ``cairo`` backend of ``matplotlib``.

.. _mplcairo: https://github.com/matplotlib/mplcairo

Via ``pip``
~~~~~~~~~~~

``bewegung`` can easily be installed with Python's package manager ``pip`` in a **minimal configuration** as it has only one "hard" Python dependency, `the Pillow library`_:

.. code:: bash

    pip install -vU bewegung

.. _the Pillow library: https://pillow.readthedocs.io

All further Python dependencies are optional and allow to use certain optional components of ``bewegung``. A **complete installation** of all Python components and development tools involves the installation of a number of prerequisites. On a Debian/Ubuntu Linux system for instance, those can be installed as follows:

.. code:: bash

    sudo apt-get install \
        build-essential pkg-config \
        python3-venv python3-dev \
        libcairo2 libcairo2-dev \
        gir1.2-gtk-3.0 libgirepository1.0-dev \
        libpango-1.0-0 libpango1.0-dev \
        libpangocairo-1.0-0 \
        ffmpeg

.. warning::

    The names of packages and the overall installation procedure of the mentioned prerequisites do vary between different Linux distributions and operating systems.

Once all prerequisites are present, ``bewegung`` can be installed. It is recommended to install it into a new virtual environment:

.. code:: bash

    python3 -m venv env # create virtual environment
    source env/bin/activate # activate virtual environment
    pip install -vU pip setuptools wheel # install & update setup toolchain

The actual installation of ``bewegung`` can now be triggered as follows:

.. code:: bash

    pip install -vU bewegung[all] # install bewegung

Validate Installation
~~~~~~~~~~~~~~~~~~~~~

You can directly run the `standard demo`_ of ``bewegung``:

.. _standard demo: https://github.com/pleiszenburg/bewegung/blob/master/demo/demo.py

.. code:: bash

    curl https://raw.githubusercontent.com/pleiszenburg/bewegung/master/demo/demo.py | python3

This resulting ``video.mp4`` file should look like this:

.. |standard_demo| image:: https://img.youtube.com/vi/4NFXQ73weMA/sddefault.jpg
	:target: https://www.youtube.com/watch?v=4NFXQ73weMA
	:alt: bewegung standard demo

|standard_demo|

.. _detailedinstallation:

Detailed Installation Options (``pip``)
---------------------------------------

.. note::

    This section is only relevant if you install ``bewegung`` with ``pip``.

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
- ``mplcairo`` (optional, but :ref:`highly recommended <acceleratingmatplotlib>`)

The `cairo library`_ and its headers must be installed, see `pycairo's documentation`_.

.. note::

    If ``mplcairo`` can not be installed or is not present for whatever reason, ``bewegung`` will show a warning and fall back to ``matplotlib``'s internal ``cairo`` backend.

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
