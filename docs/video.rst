.. _video:

Videos
======

``Video`` objects define and structure animations. They hold information on the *width*, *height*, *frames per second* and *length* of the video. Once a ``Video`` object has been created, it exposes *decorator methods* for user-defined :ref:`sequence classes <sequences>`, :ref:`prepare task methods <prepare_tasks>` and :ref:`layer task methods <layer_tasks>`. After the decoration of all relevant user-defined classes and methods, a video can be *rendered*. Alternatively, individual frames can be extracted as still-images. In the latter case, a ``Video`` object must be *reset* at least once in advance. The rendering of videos is fully parallelized. ``Video`` objects can use different *encoders* for generating the actual video file.

``Video`` objects provide access to :ref:`different canvas types and backends <drawing>`, see :meth:`bewegung.Video.canvas`. ``Video`` objects can, of required, manage a *context dictionary* for user-defined information, see :attr:`bewegung.Video.ctx`, which is exposed to all sequences, prepare tasks and layer tasks. ``Video`` objects also manage two :class:`bewegung.IndexPool` objects - one for prepare tasks, see :attr:`bewegung.Video.preporder`, and one for layer tasks, see :attr:`bewegung.Video.z-index`.

The ``Video`` Class
-------------------

.. autoclass:: bewegung.Video
    :members:
