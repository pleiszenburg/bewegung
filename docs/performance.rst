.. _performance:

Performance
===========

.. _typecheckingperformance:

Type Checking
-------------

``bewegung`` can enforce `type hints`_ with `typeguard`_ at runtime, which is very slow but useful for debugging. If ``typeguard`` is installed, ``bewegung`` will in fact automatically activate it.

For significantly more rendering speed, please run Python in "optimized mode 1" (``opt-1``), either using the ``-o`` `command line switch on the Python interpreter`_ or by setting the ``PYTHONOPTIMIZE`` `environment variable`_ to ``1``. Do not use "optimized mode 2" (``opt-2``) because it will cause incompatibilities and crashes. Running Python in "optimized mode 1" will deactivate both ``typeguard`` (if installed) and all of ``bewegung``'s internal assertion checks. For further details, please also see `typeguard's documentation`_.

.. _type hints: https://www.python.org/dev/peps/pep-0484/
.. _typeguard: https://github.com/agronholm/typeguard
.. _command line switch on the Python interpreter: https://docs.python.org/3/using/cmdline.html#cmdoption-o
.. _environment variable: https://docs.python.org/3/using/cmdline.html#envvar-PYTHONOPTIMIZE
.. _typeguard's documentation: https://typeguard.readthedocs.io

Pillow & SIMD
-------------

``bewegung`` is, in many ways, built around `Pillow`_. In certain cases, e.g. huge numbers of layers, high resolutions or intense sub-pixel rendering, Pillow may become a bottleneck. There is a faster version of Pillow called `Pillow-SIMD`_, which can be used as a drop-in replacement for Pillow. It can - *potentially* - offer performance improvements. Pillow-SIMD is based on `single instruction multiple data`_ (SIMD) instruction set extensions. ``bewegung`` is by default installed with Pillow as a dependency. A user can however subsequently choose to manually uninstall Pillow and install Pillow-SIMD instead. In this case, ``bewegung`` will automatically use Pillow-SIMD.

.. _Pillow: https://pillow.readthedocs.io/
.. _Pillow-SIMD: https://github.com/uploadcare/pillow-simd
.. _single instruction multiple data: https://en.wikipedia.org/wiki/Streaming_SIMD_Extensions

The following benchmark is based on ``bewegung``'s standard demo video. Pillow-SIMD was built with AVX2 support. It was measured on an AMD Epyc 7401P CPU. For consistent results, the CPU's turbo functionality was deactivated. Python ran in "optimized mode 1" (no type checks and assertions).

============ ======== ============================ ========
resolution   Pillow 8 Pillow-SIMD 7.0.0.post3 AVX2 Speedup
             (fps)    (fps)                        (factor)
============ ======== ============================ ========
1k (Full HD) 28.04    29.59                        1.06
4k           7.98     8.55                         1.07
============ ======== ============================ ========

A 6 to 7 percent improvement could be observed. However, it should be noted that Pillow can still be faster if the CPU's turbo functionality is activated. The use of SIMD instructions typically causes the CPU to produce much more heat. If the CPU's cooling system can not remove this heat in time, the CPU makes less or even no use of its turbo functionality. Real-world performance improvements when using Pillow-SIMD instead of Pillow can therefore only be observed if the CPU is sufficiently cooled. If it is not, Pillow should be faster than Pillow-SIMD in longer running rendering sessions.

Accelerating Backends
---------------------

Certain backend libraries have slow and fast ways of using them. A really good example is ``matplotlib``, which can be :ref:`drastically accelerated <acceleratingmatplotlib>` if used right. Please consult the :ref:`chapter on drawing <drawing>` as well as the documentations of the backend libraries for further details.
