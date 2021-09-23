# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    tests/linalg/test_single2d_operations.py: Vector operations

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

from math import isnan

from hypothesis import (
    given,
    strategies as st,
)

from bewegung import Vector2D

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TESTS: INT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@given(
    x1 = st.integers(),
    y1 = st.integers(),
    x2 = st.integers(),
    y2 = st.integers(),
)
def test_add_int(x1, y1, x2, y2):

    v1 = Vector2D(x1, y1)
    v2 = Vector2D(x2, y2)

    v3 = v1 + v2

    assert v3.x == x1 + x2
    assert v3.y == y1 + y2

@given(
    x1 = st.integers(),
    y1 = st.integers(),
    x2 = st.integers(),
    y2 = st.integers(),
)
def test_sub_int(x1, y1, x2, y2):

    v1 = Vector2D(x1, y1)
    v2 = Vector2D(x2, y2)

    v3 = v1 - v2

    assert v3.x == x1 - x2
    assert v3.y == y1 - y2

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TESTS: FLOAT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@given(
    x1 = st.floats(),
    y1 = st.floats(),
    x2 = st.floats(),
    y2 = st.floats(),
)
def test_add_float(x1, y1, x2, y2):

    v1 = Vector2D(x1, y1)
    v2 = Vector2D(x2, y2)

    v3 = v1 + v2

    x3 = x1 + x2
    y3 = y1 + y2

    if isnan(x3):
        assert isnan(v3.x)
    else:
        assert v3.x == x3

    if isnan(y3):
        assert isnan(v3.y)
    else:
        assert v3.y == y3

@given(
    x1 = st.floats(),
    y1 = st.floats(),
    x2 = st.floats(),
    y2 = st.floats(),
)
def test_sub_float(x1, y1, x2, y2):

    v1 = Vector2D(x1, y1)
    v2 = Vector2D(x2, y2)

    v3 = v1 - v2

    x3 = x1 - x2
    y3 = y1 - y2

    if isnan(x3):
        assert isnan(v3.x)
    else:
        assert v3.x == x3

    if isnan(y3):
        assert isnan(v3.y)
    else:
        assert v3.y == y3
