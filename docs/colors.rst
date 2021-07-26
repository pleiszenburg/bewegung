.. _colors:

Cross-Backend Abstraction: Colors
---------------------------------

All backends work with variations of RGB, RGBA or RGBa color spaces. Some use pre-multiplied alpha values, some do not. Some accept RGB values as floats from 0.0 to 1.0, some accept RGB values as integers from 0 to 255, some expect hexadecimal notations as strings. The :class:`bewegung.Color` class tries to provide a common base for working with RGB(A) colors in different notations.

The ``Color`` API
~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.Color
    :members:
