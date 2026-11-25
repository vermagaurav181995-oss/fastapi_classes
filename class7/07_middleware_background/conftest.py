import pytest
from fastapi.testclient import TestClient

from main import REGISTERED, app, sent_emails


@pytest.fixture(autouse=True)
def reset_data():
    REGISTERED.clear()
    sent_emails.clear()
    yield
    REGISTERED.clear()
    sent_emails.clear()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
