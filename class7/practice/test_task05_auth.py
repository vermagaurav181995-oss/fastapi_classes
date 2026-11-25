import pytest


def auth_headers(client, email: str, password: str) -> dict:
    return {}


def test_register_returns_201(client):
    pytest.skip("TODO")


def test_duplicate_email_returns_409(client):
    pytest.skip("TODO")


def test_wrong_password_returns_401(client):
    pytest.skip("TODO")


def test_auth_headers_helper_works(client):
    pytest.skip("TODO")
