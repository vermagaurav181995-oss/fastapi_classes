from fastapi import FastAPI
from fastapi.testclient import TestClient

from chat import router

chat_app = FastAPI()
chat_app.include_router(router)
chat_client = TestClient(chat_app)


def test_receive_own_message():
    with chat_client.websocket_connect("/ws/chat/ana") as ws:
        assert ws.receive_json() == {"user": "system", "message": "ana joined the chat"}
        ws.send_text("hello")
        assert ws.receive_json() == {"user": "ana", "message": "hello"}


def test_two_clients_get_the_broadcast():
    with chat_client.websocket_connect("/ws/chat/ana") as ana:
        ana.receive_json()
        with chat_client.websocket_connect("/ws/chat/ben") as ben:
            ben.receive_json()
            ana.receive_json()
            ben.send_text("hi all")
            assert ana.receive_json() == {"user": "ben", "message": "hi all"}
            assert ben.receive_json() == {"user": "ben", "message": "hi all"}
