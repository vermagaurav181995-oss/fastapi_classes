import pytest


def add(a: int, b: int) -> int:
    return a + b


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-2, -3) == -5


@pytest.mark.xfail(reason="wrong on purpose: 2 + 3 is not 6", strict=True)
def test_fails_on_purpose():
    assert add(2, 3) == 6
