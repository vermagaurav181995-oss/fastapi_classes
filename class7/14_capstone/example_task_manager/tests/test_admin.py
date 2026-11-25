def test_admin_users_requires_admin(client, ana_headers, admin_headers):
    assert client.get("/admin/users").status_code == 401
    assert client.get("/admin/users", headers=ana_headers).status_code == 403
    emails = [u["email"] for u in client.get("/admin/users", headers=admin_headers).json()]
    assert emails == ["admin@example.com", "ana@example.com"]


def test_admin_stats(client, ana_headers, admin_headers):
    client.post("/projects", json={"name": "Thesis"}, headers=ana_headers)
    client.post("/projects/1/tasks", json={"title": "A"}, headers=ana_headers)
    client.post("/projects/1/tasks", json={"title": "B", "status": "done"}, headers=ana_headers)
    assert client.get("/admin/stats", headers=admin_headers).json() == {
        "users": 2, "projects": 1, "tasks": 2, "tasks_by_status": {"todo": 1, "done": 1},
    }


def test_admin_stats_forbidden_for_users(client, ana_headers):
    assert client.get("/admin/stats", headers=ana_headers).status_code == 403
