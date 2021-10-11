3D to 2D projections: A Camera
==============================

``bewegung`` includes a `pin-hole camera`_ for simple 3D to 2D projections. In a nutshell, the a :class:`bewegung.Camera` object can convert a :class:`bewegung.Vector3D` object into a :class:`bewegung.Vector2D` object given a location and direction in 3D space, i.e. the 3D vector is projected into a plane in 2D space. Because the "camera" is actually not a rendering system on its own, it simply adds meta data (:attr:`bewegung.Vector.meta`) to the returned 2D vector: The absolute distance (``meta["dist"]``) from the "pinhole" in 3D space to the vector in 3D space. This allows to (manually) implement various kinds of depth perception, e.g. backgrounds and foregrounds, in visualizations. The camera is a useful tool if e.g. multiple :ref:`drawing backends <drawing>` are combined within a single animation and some kind of common 3D visualization is required. A typical combination is :ref:`datashader <datashader>` for density distributions and :ref:`cairo <backendcairo>` for annotations on top, see :ref:`gallery <gallery>` for examples.

.. _pin-hole camera: https://en.wikipedia.org/wiki/Pinhole_camera

.. autoclass:: bewegung.Camera
    :members:
