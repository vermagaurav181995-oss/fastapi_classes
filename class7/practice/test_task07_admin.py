import pytest


def test_delete_without_token_is_401(client):
    pytest.skip("TODO")


def test_delete_as_normal_user_is_403(client):
    pytest.skip("TODO: register + log in a normal user first")


def test_delete_as_admin_is_204(client):
    pytest.skip("TODO: also check the book is really gone (GET -> 404)")
