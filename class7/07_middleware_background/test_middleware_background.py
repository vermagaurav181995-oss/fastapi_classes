ALLOWED = "http://localhost:5173"
BLOCKED = "http://evil.com"


def test_timing_header_is_added(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert "X-Process-Time-ms" in response.headers
    assert float(response.headers["X-Process-Time-ms"]) >= 0


def test_timing_header_on_errors_too(client):
    response = client.post("/register", json={"email": "bad"})
    assert response.status_code == 422
    assert "X-Process-Time-ms" in response.headers


def test_cors_allowed_origin(client):
    response = client.get("/ping", headers={"Origin": ALLOWED})
    assert response.headers["access-control-allow-origin"] == ALLOWED


def test_cors_blocked_origin(client):
    response = client.get("/ping", headers={"Origin": BLOCKED})
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers


def test_cors_preflight(client):
    preflight = {"Access-Control-Request-Method": "POST"}
    allowed = client.options("/register", headers={"Origin": ALLOWED, **preflight})
    blocked = client.options("/register", headers={"Origin": BLOCKED, **preflight})
    assert allowed.status_code == 200 and allowed.headers["access-control-allow-origin"] == ALLOWED
    assert blocked.status_code == 400


def test_background_task_ran(client):
    response = client.post("/register", json={"email": "ana@example.com", "password": "anapass123"})
    assert response.status_code == 201
    from main import sent_emails

    assert sent_emails == ["ana@example.com"]


def test_no_background_task_when_request_fails(client):
    client.post("/register", json={"email": "ana@example.com", "password": "anapass123"})
    assert client.post("/register", json={"email": "ana@example.com", "password": "anapass123"}).status_code == 409
    from main import sent_emails

    assert sent_emails == ["ana@example.com"]
