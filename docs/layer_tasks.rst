.. _layer_tasks:

Layer Tasks
===========

Layer tasks are special, decorated methods within user-defined :ref:`sequence <sequences>` classes. They allow to "draw an image" once per frame. Similar to :ref:`prepare task methods <prepare_tasks>`, they are evaluated in a certain order, the ``z-index``. A :ref:`pool <index_pool>` of z-index-values is managed by :attr:`bewegung.Video.zindex` once per video. Layer tasks can :ref:`request parameters on demand <requesting_parameters>`.

Layers can be configured to use a certain :ref:`backend for drawing <drawing>`. ``DrawingBoard`` is the default backend, see :ref:`here <drawingboard>`. It does not matter what kind of object a layer method returns as long as it is recognized by one of the currently loaded backends. If the canvas was provided by ``bewegung``, a layer method usually does not need to return it - ``bewegung`` will keep a reference on it. There are exceptions however: The :ref:`datashader backend <datashader>` for instance requires the user to convert the canvas to an image before the user must in fact return the image from the layer method.

Layers may have an *offset* from the top-left corner of the video frame, where the y-axes is positive downwards. The size, i.e. width and height, of a layer must be configured through its backend via the :meth:`bewegung.Video.canvas` method.

Layers can be post-processed by an arbitrary number of :ref:`effects`. Effects are special decorator classes which are stacked on top of the :meth:`bewegung.Video.layer` decorator method.

The ``Video.layer`` Decorator
-----------------------------

This method is used to decorate layer task methods within user-defined :ref:`sequence <sequences>` classes. See :meth:`bewegung.Video.layer` method for further details.

The ``Layer`` Class
-------------------

.. warning::

    Do not work with this class directly. Use the :meth:`bewegung.Video.layer` method instead.

.. autoclass:: bewegung.animation.Layer
    :members:
    :private-members:
