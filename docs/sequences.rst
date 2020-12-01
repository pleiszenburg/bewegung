.. _sequences:

Sequences
=========

A *sequence* is a *time-span within a video*. A sequence can hold multiple :ref:`prepare tasks <prepare_tasks>` and :ref:`layer tasks <layer_tasks>`. Every prepare task and layer task is evaluated once per video frame, if the video frames is *within the temporal boundaries* of the sequence.

From a practical point of view, sequences are special user-defined and decorated classes. A user must not instantiate a sequence class. Prepare tasks and layer tasks are special, also decorated methods within those user-defined classes. If a constructor method is present in the user-defined sequence class, it is evaluated once per video rendering run. It is also (re-) evaluated if the video object is reset. User-defined sequence classes are eventually "mixed" with the :class:`bewegung.Sequence` class. All of its methods and properties are therefore available in user-defined sequence classes.

The ``Video.sequence`` Decorator
--------------------------------

This method is used to decorate user-defined sequence classes. See :meth:`bewegung.Video.sequence` method for further details.

The ``Sequence`` Class
----------------------

.. warning::

    Do not work with this class directly. Use the :meth:`bewegung.Video.sequence` method instead.

.. autoclass:: bewegung.core.sequence.Sequence
    :members:
