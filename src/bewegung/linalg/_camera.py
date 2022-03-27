# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    src/bewegung/linalg/_camera.py: Simple pinhole camera

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

import math
import sys
from typing import Union

try:
    from numba import jit, float32, float64, boolean
except ModuleNotFoundError:
    def jit(*jit_args, **jit_kwargs):
        def wrapper(func):
            return func
        return wrapper
    boolean, float32, float64 = None, tuple(), tuple()

from ..lib import typechecked
from ._abc import CameraABC
from ._matrix import Matrix
from ._numpy import np
from ._single2d import Vector2D
from ._single3d import Vector3D
from ._array2d import VectorArray2D
from ._array3d import VectorArray3D

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@typechecked
class Camera(CameraABC):
    """
    A virtual camera for 3D to 2D projections.
    3D vectors are projected onto a 2D plane and returned combined with the absolute distance to the camera in 3D space.
    Vector arrays can be handled if ``numpy`` and ``numba`` are present.

    Mutable.

    Args:
        position : Position in 3D space
        direction : Direction of view in 3D space
        roll : Roll angle in radians
        planeOffset : Center offset of 2D plane
        planeFactor : Scaling factor for the 2D plane
        planeYFlip : Allows to invert y-axes of 2D plane, i.e. switch to positive downwards
    """

    def __init__(self,
        position: Union[Vector3D, None] = None,
        direction: Union[Vector3D, None] = None,
        roll: float = 0.0,
        planeOffset: Union[Vector2D, None] = None,
        planeFactor: float = 1.0,
        planeYFlip: bool = False,
    ):

        # camera position
        self._position = Vector3D(0.0, 0.0, 0.0) if position is None else position
        # 3D view vector
        self._direction = Vector3D(1.0, 0.0, 0.0) if direction is None else direction
        if not math.isclose(self._direction.mag, 1.0):
            self._direction.mul(1.0 / self._direction.mag)
        self._roll = roll

        # Center offset on 2D rendering plane
        self._planeOffset = Vector2D(0.0, 0.0) if planeOffset is None else planeOffset
        # plane scale factor
        self._planeFactor = planeFactor
        # place Y flip
        self._planeYFlip = planeYFlip

        # 2D rendering plane in 3D space
        self._planeX = Vector3D(0.0, 0.0, 0.0)
        self._planeY = Vector3D(0.0, 0.0, 0.0)
        # compute rendering plane
        self._update_plane()

    def __repr__(self) -> str:

        return (
            '<Camera '
            f'id={id(self):x} '
            f'x={self._position.x:e} y={self._position.y:e} z={self._position.z:e} '
            f'dx={self._direction.x:e} dy={self._direction.y:e} dz={self._direction.z:e}>'
            )

    def _update_plane(self):

        _, theta, phi = self._direction.as_polar_tuple()
        theta = (math.pi / 2) - theta

        directionXYmag = Vector2D(
            x = self._direction.x,
            y = self._direction.y,
            ).mag
        SinTheta = math.sin(theta)
        tmp = 1.0 / Vector3D(
            x = self._direction.x * SinTheta,
            y = self._direction.y * SinTheta,
            z = -directionXYmag,
            ).mag

        self._planeX.update(
            x = math.sin(phi),
            y = -math.cos(phi),
            z = 0.0,
            )
        self._planeY.update(
            x = self._direction.x * SinTheta * tmp,
            y = self._direction.y * SinTheta * tmp,
            z = -directionXYmag * tmp,
            )

        assert math.isclose(self._planeX.mag, 1.0)
        assert math.isclose(self._planeY.mag, 1.0)

        if self._roll == 0:
            return

        R = Matrix.from_3d_rotation(v = self._direction, a = self._roll)
        self._planeX = R @ self._planeX
        self._planeY = R @ self._planeY

    @property
    def direction(self) -> Vector3D:
        """
        Direction of view in 3D space
        """

        return self._direction

    @direction.setter
    def direction(self, value: Vector3D):
        """
        Direction of view in 3D space
        """

        self._direction.update_from_vector(value)
        if not math.isclose(self._direction.mag, 1.0):
            self._direction.mul(1.0 / self._direction.mag)
        self._update_plane()

    @property
    def roll(self) -> float:
        """
        Roll angle in radians
        """

        return self._roll

    @roll.setter
    def roll(self, value: float):
        """
        Roll angle in radians
        """

        self._roll = value
        self._update_plane()

    @property
    def position(self) -> Vector3D:
        """
        Position in 3D space
        """

        return self._position

    @position.setter
    def position(self, value: Vector3D):
        """
        Position in 3D space
        """

        self._position.update_from_vector(value)

    @property
    def planeFactor(self) -> float:
        """
        Scaling factor for the 2D plane
        """

        return self._planeFactor

    @planeFactor.setter
    def planeFactor(self, value: float):
        """
        Scaling factor for the 2D plane
        """

        self._planeFactor = value

    @property
    def planeOffset(self) -> Vector2D:
        """
        Center offset of 2D plane
        """

        return self._planeOffset

    @planeOffset.setter
    def planeOffset(self, value: Vector2D):
        """
        Center offset of 2D plane
        """

        self._planeOffset.update_from_vector(value)

    @property
    def planeYFlip(self) -> bool:
        """
        Allows to invert y-axes of 2D plane, i.e. switch to positive downwards
        """

        return self._planeYFlip

    @planeYFlip.setter
    def planeYFlip(self, value: bool):
        """
        Allows to invert y-axes of 2D plane, i.e. switch to positive downwards
        """

        self._planeYFlip = value

    def get_point(self, point3D: Vector3D) -> Vector2D:
        """
        Projects a 3D vector onto a 2D plane.
        Returns a 2D vector combined with the absolute distance to the camera in 3D space (``meta["dist"]``).

        Args:
            point3D : point in 3D space
        """

        ma = [
            [self._planeX.x, self._planeY.x, -(point3D.x - self._position.x), -self._direction.x],
            [self._planeX.y, self._planeY.y, -(point3D.y - self._position.y), -self._direction.y],
            [self._planeX.z, self._planeY.z, -(point3D.z - self._position.z), -self._direction.z],
            ]

        determ = (
              ma[0][0] * ma[1][1] * ma[2][2]
            + ma[0][1] * ma[1][2] * ma[2][0]
            + ma[0][2] * ma[1][0] * ma[2][1]
            - ma[0][2] * ma[1][1] * ma[2][0]
            - ma[0][0] * ma[1][2] * ma[2][1]
            - ma[0][1] * ma[1][0] * ma[2][2]
            )

        if determ == 0.0:
            determ = sys.float_info.min # HACK

        point2D = Vector2D(
            x = (
                  ma[0][3] * ma[1][1] * ma[2][2]
                + ma[0][1] * ma[1][2] * ma[2][3]
                + ma[0][2] * ma[1][3] * ma[2][1]
                - ma[0][2] * ma[1][1] * ma[2][3]
                - ma[0][3] * ma[1][2] * ma[2][1]
                - ma[0][1] * ma[1][3] * ma[2][2]
                ) / determ,
            y = (
                  ma[0][0] * ma[1][3] * ma[2][2]
                + ma[0][3] * ma[1][2] * ma[2][0]
                + ma[0][2] * ma[1][0] * ma[2][3]
                - ma[0][2] * ma[1][3] * ma[2][0]
                - ma[0][0] * ma[1][2] * ma[2][3]
                - ma[0][3] * ma[1][0] * ma[2][2]
                ) / determ,
            )

        if self._planeYFlip:
            point2D.y = -point2D.y

        point2D.x *= self._planeFactor
        point2D.y *= self._planeFactor
        point2D += self._planeOffset

        return Vector2D(
            x = point2D.x,
            y = point2D.y,
            meta = dict(dist = (point3D - self._position).mag),
            )

    def get_points(self, points3d: VectorArray3D) -> VectorArray2D:
        """
        Projects a 3D vector array onto a 2D plane.
        Returns a 2D vector array combined with the absolute distances to the camera in 3D space (``meta["dist"]``).

        Args:
            points3d : points in 3D space
        """

        if np is None:
            raise NotImplementedError('numpy is not available')

        position = self._position.as_ndarray() # type
        planeOffset = self._planeOffset.as_ndarray() # type
        points3d = points3d.as_ndarray() # type
        planeFactor = np.float32(self._planeFactor) # type

        ma = np.array([
            [self._planeX.x, self._planeY.x, 0.0, -self._direction.x],
            [self._planeX.y, self._planeY.y, 0.0, -self._direction.y],
            [self._planeX.z, self._planeY.z, 0.0, -self._direction.z],
            ], dtype = points3d.dtype) # type / matrix
        empty = np.array([
            np.nan,
            np.nan,
            np.nan,
            ], dtype = points3d.dtype) # NaN placeholder
        points2d = np.zeros(points3d.shape, dtype = points3d.dtype) # type / target

        self._get_points_jit(
            points3d, points2d,
            ma, position, empty, planeOffset,
            planeFactor, self._planeYFlip,
            )

        return VectorArray2D(
            x = points2d[:, 0],
            y = points2d[:, 1],
            meta = dict(dist = points2d[:, 2]),
            )

    @staticmethod
    @jit(
        [
            (
                float32[:, :], float32[:, :],
                float32[:, :], float32[:], float32[:], float32[:],
                float32, boolean,
            ), (
                float64[:, :], float64[:, :],
                float64[:, :], float64[:], float64[:], float64[:],
                float64, boolean,
            )
        ],
        nopython = True,
    )
    def _get_points_jit(
        points_3d, points_2d,
        ma, position, empty, planeOffset,
        planeFactor, planeYFlip,
        ):

        for index in range(0, points_3d.shape[0]):

            ma[:, 2] = position - points_3d[index, :]

            determ = (
                  ma[0][0] * ma[1][1] * ma[2][2]
                + ma[0][1] * ma[1][2] * ma[2][0]
                + ma[0][2] * ma[1][0] * ma[2][1]
                - ma[0][2] * ma[1][1] * ma[2][0]
                - ma[0][0] * ma[1][2] * ma[2][1]
                - ma[0][1] * ma[1][0] * ma[2][2]
                )

            if determ == 0:
                points_2d[index, :] = empty
                continue

            points_2d[index, 0] = (
                  ma[0][3] * ma[1][1] * ma[2][2]
                + ma[0][1] * ma[1][2] * ma[2][3]
                + ma[0][2] * ma[1][3] * ma[2][1]
                - ma[0][2] * ma[1][1] * ma[2][3]
                - ma[0][3] * ma[1][2] * ma[2][1]
                - ma[0][1] * ma[1][3] * ma[2][2]
                )
            points_2d[index, 1] = (
                  ma[0][0] * ma[1][3] * ma[2][2]
                + ma[0][3] * ma[1][2] * ma[2][0]
                + ma[0][2] * ma[1][0] * ma[2][3]
                - ma[0][2] * ma[1][3] * ma[2][0]
                - ma[0][0] * ma[1][2] * ma[2][3]
                - ma[0][3] * ma[1][0] * ma[2][2]
                )

            points_2d[index, :2] *= planeFactor / determ
            if planeYFlip:
                points_2d[index, 1] = -points_2d[index, 1]
            points_2d[index, :2] += planeOffset

            points_2d[index, 2] = np.sqrt(np.sum(np.power(points_3d[index, :] - position, 2))) # distance
