# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/animation/_backends/_base.py: Backend base class

    Copyright (C) 2020-2022 Sebastian M. Ernst <ernst@pleiszenburg.de>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU Lesser General Public License
Version 2.1 ("LGPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
https://github.com/pleiszenburg/bewegung/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from typing import Any, Callable, Type

from PIL.Image import Image

from ...lib import typechecked
from .._abc import BackendABC, VideoABC

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class BackendBase(BackendABC):
    """
    Base class for backends. Do not instantiate this class - derive and inherit from it instead.

    Backend objects are mutable.

    If the orginal cunstructor method is overridden, it must be called from the child class.
    """

    _name = None

    def __init__(self):
        """
        Can be overridden.
        """

        self._loaded = False
        self._type = None

    def __repr__(self) -> str:
        """
        Interactive string representation of backend object

        Do not override!
        """

        if self._name is not None:
            return f'<{self._name:s}Backend>'

        return f'<{type(self).__name__:s}>'

    def prototype(self, video: VideoABC, **kwargs) -> Callable:
        """
        Returns a factory function which produces a new canvas once per call

        Do not override!

        Args:
            video : A video object
            kwargs : Keyword arguments for the backend library
        """

        if not self._loaded:
            self.load()

        return self._prototype(video, **kwargs)

    def _prototype(self, video: VideoABC, **kwargs) -> Callable:
        """
        Internal method: Returns a factory function which produces a new canvas once per call

        Must be reimplemented!

        Args:
            video : A video object
            kwargs : Keyword arguments for the backend library
        """

        raise NotImplementedError()

    def isinstance(self, obj: Any, hard: bool = True) -> bool:
        """
        Checks whether or not a certain object is an allowed return type within the backend

        Do not override!

        Args:
            obj : The objects which is supposed to be checked
            hard : If set to ``True`` when the backend is not loaded, the backend will not be loaded for the check and the test will therefore always fail (return ``False``).
        """

        if (not self._loaded) and hard:
            return False
        if not self._loaded:
            self.load()

        return self._isinstance(obj)

    def _isinstance(self, obj: Any) -> bool:
        """
        Internal method: Checks whether or not a certain object is an allowed return type within the backend

        Can be reimplemented.

        Args:
            obj : The objects which is supposed to be checked
        """

        return isinstance(obj, self._type)

    def load(self):
        """
        Orders the backend to import its dependencies (libraries)

        Do not override!
        """

        if self._loaded:
            return

        self._load()
        assert self._type is not None

        self._loaded = True

    def _load(self):
        """
        Internal method: Orders the backend to import its dependencies (libraries)

        Must be reimplemented!
        """

        raise NotImplementedError()

    def to_pil(self, obj: Any) -> Image:
        """
        Converts canvas to Pillow Image object

        Do not override!

        Args:
            obj : Backend canvas object
        """

        if not self._loaded:
            self.load()
        if not self._isinstance(obj):
            raise TypeError('unkown / unhandled canvas type')

        return self._to_pil(obj)

    def _to_pil(self, obj: Any) -> Image:
        """
        Internal method: Converts canvas to Pillow Image object

        Must be reimplemented!

        Args:
            obj : Backend canvas object
        """

        raise NotImplementedError()

    @property
    def loaded(self) -> bool:
        """
        Status: Has the backend imported its dependencies?

        Do not override!
        """

        return self._loaded

    @property
    def type(self) -> Type:
        """
        Exposes backends canvas class

        Do not override!
        """

        if not self._loaded:
            self.load()

        return self._type
