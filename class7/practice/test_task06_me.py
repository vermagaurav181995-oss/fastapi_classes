import pytest


def test_me_without_token(client):
    pytest.skip("TODO: 401, detail 'Not authenticated'")


def test_me_with_fake_token(client):
    pytest.skip("TODO: 401, detail 'Could not validate credentials'")


def test_me_with_real_token(client):
    pytest.skip("TODO: register, log in, GET /auth/me -> 200 and the right email")


def test_me_with_expired_token(client):
    pytest.skip("TODO (bonus)")
