.. _debug:

Debugging
=========

Type Checking at Runtime
------------------------

``bewegung`` enforces `type hints`_ with `typeguard`_ at runtime by default - if ``typeguard`` is installed. Any kind of type violation triggers an exception.

.. warning::

    Type checking at runtime is a slow process. :ref:`Deactivate for better performance! <typecheckingperformance>`

.. _type hints: https://www.python.org/dev/peps/pep-0484/
.. _typeguard: https://github.com/agronholm/typeguard
