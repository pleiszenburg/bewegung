Compositing: Anatomy of a Video
===============================

Based on *layers* and *sequences*, ``bewegung`` offers a lot of infrastructure for compositing animations and videos. At its core, there is :ref:`time <time>`. It is primarily measured in frame numbers (the :attr:`bewegung.Time.index`), but can also be converted to seconds (:attr:`bewegung.Time.seconds`). Time is described using :class:`bewegung.Time` objects. A :ref:`video <video>` is fundamentally defined using the :class:`bewegung.Video` class. It offers decorators for :ref:`sequence classes <sequences>`, :ref:`prepare task methods <prepare_tasks>` and :ref:`layer task methods <layer_tasks>`. Prepare tasks and layer tasks are ordered using indices, which are managed by :ref:`index pools <index_pool>`. :ref:`Effects <effects>` can be applied to individual layers. Animations can be rendered in their entirety (see :meth:`bewegung.Video.render`) while frames can also be rendered individually (see :meth:`bewegung.Video.render_frame`). The process of rendering videos is fully parallelized. ``bewegung`` supports different :ref:`encoders <encoders>`.

.. toctree::
   :maxdepth: 2
   :caption: The Individual Pieces Explained

   time
   video
   sequences
   pool
   prepare_tasks
   layer_tasks
   effects
   encoders
