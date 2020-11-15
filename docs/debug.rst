.. _debug:

Debugging & Performance
=======================

``bewegung`` can enforce `type hints`_ with `typeguard`_ at runtime, which is very slow but useful for debugging. If ``typeguard`` is installed, ``bewegung`` will in fact automatically activate it.

For significantly more rendering speed, please run Python in "optimized mode 1" (`opt-1`), either using the ``-o`` `command line switch on the Python interpreter`_ or by setting the ``PYTHONOPTIMIZE`` `environment variable`_ to ``1``. Do not use "optimized mode 2" (`opt-2`) because it will cause incompatibilities and crashes. Running Python in "optimized mode 1" will deactivate both ``typeguard`` (if installed) and all of ``bewegung``'s internal assertion checks. For further details, please also see `typeguard's documentation`_.

.. _type hints: https://www.python.org/dev/peps/pep-0484/
.. _typeguard: https://github.com/agronholm/typeguard
.. _command line switch on the Python interpreter: https://docs.python.org/3/using/cmdline.html#cmdoption-o
.. _environment variable: https://docs.python.org/3/using/cmdline.html#envvar-PYTHONOPTIMIZE
.. _typeguard's documentation: https://typeguard.readthedocs.io
