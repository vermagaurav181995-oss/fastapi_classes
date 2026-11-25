import pytest

from test_math import add


@pytest.mark.skip(reason="Remove this line to see what a failing test looks like")
def test_add_is_wrong_on_purpose():
    expected = 6
    assert add(2, 3) == expected
