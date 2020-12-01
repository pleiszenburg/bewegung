.. _prepare_tasks:

Prepare Tasks
=============

Prepare tasks are special, decorated methods within user-defined :ref:`sequence <sequences>` classes. They allow to *prepare* and compute data once per frame. Similar to :ref:`layer task methods <layer_tasks>`, they are evaluated in a certain order, the ``prepoder``. A :ref:`pool <index_pool>` of prepoder-values is managed by :attr:`bewegung.Video.prepoder` once per video. Prepare tasks can :ref:`request parameters on demand <requesting_parameters>`.

The ``Video.prepare`` Decorator
-------------------------------

This method is used to decorate prepare task methods within user-defined :ref:`sequence <sequences>` classes. See :meth:`bewegung.Video.prepare` method for further details.
