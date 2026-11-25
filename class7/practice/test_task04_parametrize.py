import pytest

INVALID_PAYLOADS = [
]


@pytest.mark.parametrize("payload", INVALID_PAYLOADS or [None])
def test_invalid_book_returns_422(client, payload):
    pytest.skip("TODO")
