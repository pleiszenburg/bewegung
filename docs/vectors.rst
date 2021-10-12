.. _vectors:

Vectors and Vector Arrays
=========================

``bewegung`` offers :ref:`vectors <vector_single>` and :ref:`vector arrays <vector_array>`. Both of them are available in 2D and 3D variants. Both vectors and vector arrays can interact with each other as well as with :ref:`matrices <matrices>`.

.. note::

    Besides simple vector algebra, a lot of ``bewegung``'s functions and methods expect geometric input using vector objects.

.. _vector_single:

Vector Classes
--------------

The vector classes describe individual vectors in 2D and 3D space. Vectors are "statically typed", i.e. all components are of one single type, and use Python number types (sub-classes of ``numbers.Number``). The data type of a vector is exposed through its ``dtype`` property.

The ``Vector`` base class
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.Vector
    :members:

The ``Vector2D`` class
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.Vector2D
    :members:

The ``Vector3D`` class
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.Vector3D
    :members:

.. _vector_array:

Vector Array Classes
--------------------

The vector array classes describe arrays of individual vectors in 2D and 3D space. Vector arrays are "statically typed" and use ``numpy`` arrays for storing data. Just like ``numpy.ndarray`` objects, they expose a ``dtype`` property.

The ``VectorArray`` base class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.VectorArray
    :members:

The ``VectorArray2D`` class
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.VectorArray2D
    :members:

The ``VectorArray3D`` class
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.VectorArray3D
    :members:
