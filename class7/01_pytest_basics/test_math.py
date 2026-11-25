def add(a: int, b: int) -> int:
    return a + b


def test_add_two_positive_numbers():
    a, b = 2, 3
    result = add(a, b)
    assert result == 5


def test_add_negative_numbers():
    assert add(-2, -3) == -5
    assert add(-2, 2) == 0
