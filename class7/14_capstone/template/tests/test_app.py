def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_timing_header(client):
    assert "X-Process-Time-ms" in client.get("/health").headers


def test_cors_allowed_origin(client):
    response = client.get("/health", headers={"Origin": "http://localhost:5173"})
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_items_are_not_implemented_yet(client, ana_headers):
    assert client.get("/items", headers=ana_headers).status_code == 501
