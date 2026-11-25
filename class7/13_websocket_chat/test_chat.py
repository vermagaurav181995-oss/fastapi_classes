from fastapi.testclient import TestClient

from chat import manager
from main import app

client = TestClient(app)


def test_chat_page_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>Chat</h1>" in response.text


def test_one_client_receives_its_own_message():
    with client.websocket_connect("/ws/chat/ana") as ana:
        assert ana.receive_json() == {"user": "system", "message": "ana joined the chat"}
        ana.send_text("hello")
        assert ana.receive_json() == {"user": "ana", "message": "hello"}


def test_two_clients_both_receive_a_broadcast():
    with client.websocket_connect("/ws/chat/ana") as ana:
        ana.receive_json()
        with client.websocket_connect("/ws/chat/ben") as ben:
            assert ben.receive_json()["message"] == "ben joined the chat"
            assert ana.receive_json()["message"] == "ben joined the chat"

            ana.send_text("hi ben")
            expected = {"user": "ana", "message": "hi ben"}
            assert ana.receive_json() == expected
            assert ben.receive_json() == expected

        assert ana.receive_json() == {"user": "system", "message": "ben left the chat"}


def test_disconnect_removes_the_connection():
    with client.websocket_connect("/ws/chat/ana") as ana:
        ana.receive_json()
        assert len(manager.active_connections) == 1
    assert len(manager.active_connections) == 0
