.. _vectors:

Vectors and Vector Arrays
=========================

``bewegung`` offers :ref:`vectors <vector_single>` and :ref:`vector arrays <vector_array>`. Both of them are available in 2D and 3D variants. In 2D space, there are additional variants exposing a "distance property". The distance can be used to describe a (relative) distance to a camera or observer, which is useful for various types of renderings. Finally, there is also a :ref:`matrix <matrix>` for simple tasks like rotations both in 2D and 3D space.

.. note::

    Besides simple vector algebra, a lot of ``bewegung``'s functions and methods expect geometric input using vector classes.

.. _vector_single:

Vector Classes
--------------

The vector classes describe individual vectors in 2D and 3D space. Vectors are "statically typed", use Python number types and can either have ``int`` or ``float`` components. The data type of a vector is exposed through its ``dtype`` property.

The ``Vector2D`` class
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.Vector2D
    :members:

The ``Vector2Ddist`` class
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.Vector2Ddist
    :members:

The ``Vector3D`` class
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.Vector3D
    :members:

.. _vector_array:

Vector Array Classes
--------------------

The vector array classes describe arrays of individual vectors in 2D and 3D space. Vector arrays are "statically typed" and use ``numpy`` arrays for storing data. Just like ``numpy.ndarray`` objects, they expose a ``dtype`` property.

The ``VectorArray2D`` class
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.VectorArray2D
    :members:

The ``VectorArray2Ddist`` class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.VectorArray2Ddist
    :members:

The ``VectorArray3D`` class
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.VectorArray3D
    :members:

.. _matrix:

The ``Matrix`` Class
--------------------

.. autoclass:: bewegung.Matrix
    :members:
