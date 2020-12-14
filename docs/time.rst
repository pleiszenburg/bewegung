.. _time:

Time
====

Describing and handling *time* is a core functionality of ``bewegung``. While the library works with *discrete frame numbers* (also referred to as the *index*) internally, a user may want to interact with *time in seconds*. :class:`bewegung.Time` objects allow to do both. They handle the conversion between the two based on their internal *frames per second* state. :class:`bewegung.Time` objects support basic arithmetic.

.. note::

    :class:`bewegung.Time` objects are expected to have an identical *frames per second* state across a video. The :meth:`bewegung.Time.time` and :meth:`bewegung.Time.time_from_seconds` methods offer facilities for generating new :class:`bewegung.Time` objects while "inheriting" the *frames per second* state from an existing :class:`bewegung.Time` object. The :meth:`bewegung.Video.time` and :meth:`bewegung.Video.time_from_seconds` methods do exactly the same thing based on a :class:`bewegung.Video` object's *frames per second* state.

.. warning::

    Operations between :class:`bewegung.Time` objects with a different *frames per second* state will fail, i.e. raise an exception.

An animation is very likely representing real-world data in some slowed-down or accelerated way, i.e. as a form of a *slow-motion* or *time-lapse* video. ``bewegung`` allows to convert time from custom formats to its internal system via the :class:`bewegung.TimeScale` class.

The ``Time`` Class
------------------

.. autoclass:: bewegung.Time
    :members:

The ``TimeScale`` Class
-----------------------

.. autoclass:: bewegung.TimeScale
    :members:
