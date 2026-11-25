def test_timing_header(client):
    assert "X-Process-Time-ms" in client.get("/books").headers


def test_cors_allowed_origin(client):
    response = client.get("/books", headers={"Origin": "http://localhost:5173"})
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_blocked_origin(client):
    response = client.get("/books", headers={"Origin": "http://evil.com"})
    assert "access-control-allow-origin" not in response.headers
