.. _index_pool:

Index Pools
===========

``IndexPool`` objects are meant to manage index values that are fed into the ``preporder`` parameter of the :meth:`bewegung.Video.prepare` decorator method and the ``zindex`` parameter of the :meth:`bewegung.Video.layer` decorator method. A ``Video`` object therefore manages two pools: :attr:`bewegung.Video.zindex` and :attr:`bewegung.Video.preporder`.

The ``IndexPool`` Class
-----------------------

.. autoclass:: bewegung.IndexPool
    :members:
