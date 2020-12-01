.. _encoders:

Encoders
========

Encoder objects are passed to the ``encoder`` parameter of :meth:`bewegung.Video.render`. While ``bewegung`` handles the composition of video frames, the completed frames are streamed to an actual video encoding tool or library. It is possible to define custom encoders.

Available Encoders
------------------

.. autoclass:: bewegung.FFmpegH264Encoder

.. autoclass:: bewegung.FFmpegGifEncoder

Defining Custom Encoders
------------------------

Custom encoders can be defined by deriving from the :class:`bewegung.EncoderBase` class. This mechanism can be used to build both custom ``ffmpeg``-based pipelines as well as wrap other tools such as `mencoder`_.

.. _mencoder: http://www.mplayerhq.hu/DOCS/HTML/en/mencoder.html

The ``EncoderBase`` Class
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: bewegung.EncoderBase
    :members:
    :private-members:
