import pytest


def test_timing_header(client):
    pytest.skip("TODO: any GET -> 'X-Process-Time-ms' in response.headers")


def test_cors_allowed_origin(client):
    pytest.skip("TODO: send headers={'Origin': 'http://localhost:5173'} -> check access-control-allow-origin")


def test_cors_blocked_origin(client):
    pytest.skip("TODO: Origin http://evil.com -> NO access-control-allow-origin header")
