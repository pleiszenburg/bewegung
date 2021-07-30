Inventory of ``backends``
=========================

All backends can be accessed via the ``backends`` dictionary, which represents the inventory of backends.

.. code:: ipython

    >>> from bewegung import backends
    >>> backends.keys()
    dict_keys(['drawingboard', 'pillow', 'datashader', 'cairo', 'matplotlib'])
    >>> [backend for backend in backends.values()]
    [<DrawingBoardBackend>, <PillowBackend>, <DatashaderBackend>, <CairoBackend>, <MatplotlibBackend>]

Backends are "lazy" objects. They only import the underlying library if actually used. For most intents and purposes, working with :meth:`bewegung.Video.canvas` is sufficient. Further details about the common structure of backends are provided in the :ref:`sections on custom backends <custombackends>`.
