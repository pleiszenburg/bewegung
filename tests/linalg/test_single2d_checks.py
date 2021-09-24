# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    tests/linalg/test_single2d_checks.py: Vector 2D checks

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
    x1 = st.floats(),
    y1 = st.floats(),
)
def test_eq(x1, y1):

    v1 = Vector2D(x1, y1)

    if not isnan(x1) and not isnan(y1):
        assert v1 == v1
        assert v1 % v1
    else:
        assert v1 != v1
        assert not v1 % v1

    v1c = v1.copy()
    assert v1 is not v1c

    if not isnan(x1) and not isnan(y1):
        assert v1 == v1c
        assert v1 % v1c
    else:
        assert v1 != v1c
        assert not v1 % v1c

@given(
    x1 = st.integers(),
    y1 = st.integers(),
)
def test_eq_types(x1, y1):

    x1f = float(x1)
    y1f = float(y1)

    v1 = Vector2D(x1, y1)
    v1f = Vector2D(x1f, y1f)

    assert v1 % v1f

    if x1f == x1 and y1f == y1:
        assert v1f == v1
    else:
        assert v1f != v1
