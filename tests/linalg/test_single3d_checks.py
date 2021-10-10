# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    tests/linalg/test_single2d_checks.py: Vector 3D checks

    Copyright (C) 2020-2021 Sebastian M. Ernst <ernst@pleiszenburg.de>

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

from math import isnan, isclose, pi, sqrt

import numpy as np
from hypothesis import (
    given,
    strategies as st,
)
import pytest

from bewegung import Vector3D

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TESTS: INT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def test_repr():

    v1 = Vector3D(0, 0, 0)
    v2 = Vector3D(0.0, 0.0, 0.0)

    v1r = repr(v1)
    v2r = repr(v2)

    assert 'Vector3D' in v1r
    assert 'Vector3D' in v2r

    assert 'dtype=int' in v1r
    assert 'dtype=float' in v2r

@given(
    x1 = st.floats(),
    y1 = st.floats(),
    z1 = st.floats(),
)
def test_eq(x1, y1, z1):

    v1 = Vector3D(x1, y1, z1)

    if not isnan(x1) and not isnan(y1) and not isnan(z1):
        assert v1 == v1
        assert v1 % v1
    else:
        assert v1 != v1
        assert not v1 % v1

    v1c = v1.copy()
    assert v1 is not v1c

    if not isnan(x1) and not isnan(y1) and not isnan(z1):
        assert v1 == v1c
        assert v1 % v1c
    else:
        assert v1 != v1c
        assert not v1 % v1c

@given(
    x1 = st.integers(),
    y1 = st.integers(),
    z1 = st.integers(),
)
def test_eq_types(x1, y1, z1):

    x1f = float(x1)
    y1f = float(y1)
    z1f = float(z1)

    v1 = Vector3D(x1, y1, z1)
    v1f = Vector3D(x1f, y1f, z1f)

    assert v1 % v1f

    if x1f == x1 and y1f == y1 and z1f == z1:
        assert v1f == v1
    else:
        assert v1f != v1

def test_dtype_basic():

    v1 = Vector3D(0, 0, 0)
    v2 = Vector3D(0.0, 0.0, 0.0)

    assert v1 == v2
    assert v1 % v2

    v1i = v1.as_dtype(int)
    v1f = v1.as_dtype(float)

    assert v1i == v1
    assert v1i is not v1
    assert v1i.dtype == int

    assert v1f == v1
    assert v1f is not v1
    assert v1f.dtype == float

    v2i = v2.as_dtype(int)
    v2f = v2.as_dtype(float)

    assert v2i == v2
    assert v2i is not v2
    assert v2i.dtype == int

    assert v2f == v2
    assert v2f is not v2
    assert v2f.dtype == float

def test_dtype_np():

    v1 = Vector3D(np.int8(0), np.int8(0), np.int8(0))
    v2 = Vector3D(np.float32(0.0), np.float32(0.0), np.float32(0.0))

    assert v1 == v2
    assert v1 % v2

    assert v1.dtype == np.int8
    assert v2.dtype == np.float32

    v3 = v1.as_dtype(int)
    assert v3.dtype == int

    v4 = v2.as_dtype(float)
    assert v4.dtype == float

    v5 = v1 + v2
    assert v5.dtype == np.float32

def test_dtype_error():

    with pytest.raises(TypeError):
        _ = Vector3D(0, 0.0, 0.0)

    assert Vector3D(0, 0.0, 0.0, int).dtype == int
    assert Vector3D(0, 0.0, 0.0, float).dtype == float

    v1 = Vector3D(0, 0, 0, int)
    v1.update(1.0, 1.0, 1.0)
    assert v1.dtype == float
    with pytest.raises(TypeError):
        v1.update(2, 2.0, 2.0)

    assert isinstance(v1.x, float)
    assert isinstance(v1.y, float)
    assert isinstance(v1.z, float)

    with pytest.raises(TypeError):
        v1.x = 4
    with pytest.raises(TypeError):
        v1.y = 4
    with pytest.raises(TypeError):
        v1.z = 4

    v1.x = 5.0
    assert v1 == Vector3D(5.0, 1.0, 1.0)
    v1.y = 6.0
    assert v1 == Vector3D(5.0, 6.0, 1.0)
    v1.z = 7.0
    assert v1 == Vector3D(5.0, 6.0, 7.0)

def test_ndim():

    v1 = Vector3D(0, 0, 0)

    assert v1.ndim == 3

def test_extra():

    v1 = Vector3D(2, 3, 6)
    assert isinstance(v1.mag, float)
    assert isclose(v1.mag, 7.0)

    v2 = Vector3D(1, 1, 1)
    assert isinstance(v2.theta, float)
    assert isinstance(v2.phi, float)
    assert isclose(v2.theta, 0.9553166181245092)
    assert isclose(v2.phi, 0.7853981633974483)

    mag, theta, phi = v2.as_polar_tuple()
    assert isinstance(mag, float)
    assert isclose(mag, sqrt(3))
    assert isinstance(theta, float)
    assert isclose(theta, 0.9553166181245092)
    assert isinstance(phi, float)
    assert isclose(phi, 0.7853981633974483)

    assert v2 % Vector3D.from_polar(sqrt(3), 0.9553166181245092, 0.7853981633974483)
    assert v2 % Vector3D.from_geographic(sqrt(3), 45.0, 35.264389682754654)

def test_update():

    v1 = Vector3D(0, 0, 0)

    v1.update(1, 1, 1)
    assert v1.dtype == int
    assert v1 == Vector3D(1, 1, 1)

    v1.update(2.0, 2.0, 2.0)
    assert v1.dtype == float
    assert v1 == Vector3D(2.0, 2.0, 2.0)

    v2 = Vector3D(3, 3, 3)
    v1.update_from_vector(v2)
    assert v1 is not v2
    assert v1 == v2
    assert v1.dtype == int
    assert v1 == Vector3D(3, 3, 3)

    v3 = Vector3D(4.0, 4.0, 4.0)
    v1.update_from_vector(v3)
    assert v1 is not v3
    assert v1 == v3
    assert v1.dtype == float
    assert v1 == Vector3D(4.0, 4.0, 4.0)

def test_tuple():

    v1 = Vector3D(0, 0, 0)
    v2 = Vector3D(0.0, 0.0, 0.0)

    v1t = v1.as_tuple()
    v2t = v2.as_tuple()

    assert len(v1t) == 3
    assert len(v2t) == 3

    assert all(isinstance(item, int) for item in v1t)
    assert all(isinstance(item, float) for item in v2t)

    assert v1t == (0, 0, 0)
    assert v2t == (0.0, 0.0, 0.0)
