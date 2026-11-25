import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from chat import router

chat_app = FastAPI()
chat_app.include_router(router)
chat_client = TestClient(chat_app)


def test_receive_own_message():
    pytest.skip("TODO")


def test_two_clients_get_the_broadcast():
    pytest.skip("TODO: two nested websocket_connect blocks; both must receive the message")
