import pytest


def add(a: int, b: int) -> int:
    return 0


def test_add_positive_numbers():
    pytest.skip("TODO: assert add(2, 3) == 5")


def test_add_negative_numbers():
    pytest.skip("TODO: assert add(-2, -3) == -5")


def test_fails_on_purpose():
    pytest.skip("TODO: write an assert that is wrong on purpose, read the report, then mark it")
