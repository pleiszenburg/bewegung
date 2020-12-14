.. _video:

Videos
======

:class:`bewegung.Video` objects define and structure animations. They hold information on the *width*, *height*, *frames per second* and *length* of the video. Once a :class:`bewegung.Video` object has been created, it exposes *decorator methods* for user-defined :ref:`sequence classes <sequences>`, :ref:`prepare task methods <prepare_tasks>` and :ref:`layer task methods <layer_tasks>`. After the decoration of all relevant user-defined classes and methods, a video can be *rendered* by calling :meth:`bewegung.Video.render`. Alternatively, individual frames can be extracted as still-images by calling :meth:`bewegung.Video.render_frame`. In the latter case, a :class:`bewegung.Video` object must be *reset* at least once in advance by calling :meth:`bewegung.Video.reset`. The rendering of videos is fully parallelized. :class:`bewegung.Video` objects can use different :ref:`encoders <encoders>` for generating the actual video file.

:class:`bewegung.Video` objects provide access to :ref:`different canvas types and backends <drawing>`, see :meth:`bewegung.Video.canvas`. :class:`bewegung.Video` objects can, if required, manage a *context dictionary* for user-defined information, see :attr:`bewegung.Video.ctx`, which is exposed to all sequences, prepare tasks and layer tasks. :class:`bewegung.Video` objects also manage two :class:`bewegung.IndexPool` objects - one for prepare tasks, see :attr:`bewegung.Video.preporder`, and one for layer tasks, see :attr:`bewegung.Video.z-index`.

The ``Video`` Class
-------------------

.. autoclass:: bewegung.Video
    :members:
