import pytest


@pytest.fixture
def ana_project(client, ana_headers) -> dict:
    response = client.post("/projects", json={"name": "Thesis", "description": "Final year"}, headers=ana_headers)
    assert response.status_code == 201
    return response.json()


def test_create_project_sets_owner(client, ana_project):
    assert ana_project == {"id": 1, "name": "Thesis", "description": "Final year", "owner_id": 2}


def test_create_project_requires_login(client):
    assert client.post("/projects", json={"name": "X"}).status_code == 401


def test_create_project_validates_name(client, ana_headers):
    assert client.post("/projects", json={"name": ""}, headers=ana_headers).status_code == 422


def test_users_only_list_their_own_projects(client, ana_project, ben_headers):
    client.post("/projects", json={"name": "Band"}, headers=ben_headers)
    assert [p["name"] for p in client.get("/projects", headers=ben_headers).json()] == ["Band"]


def test_admin_lists_all_projects(client, ana_project, ben_headers, admin_headers):
    client.post("/projects", json={"name": "Band"}, headers=ben_headers)
    assert len(client.get("/projects", headers=admin_headers).json()) == 2


def test_list_projects_pagination(client, ana_headers):
    for name in ("A", "B", "C"):
        client.post("/projects", json={"name": name}, headers=ana_headers)
    assert [p["name"] for p in client.get("/projects?skip=1&limit=1", headers=ana_headers).json()] == ["B"]


def test_get_project_owner_200_other_403_missing_404(client, ana_project, ana_headers, ben_headers):
    assert client.get("/projects/1", headers=ana_headers).status_code == 200
    assert client.get("/projects/1", headers=ben_headers).status_code == 403
    response = client.get("/projects/99", headers=ana_headers)
    assert response.status_code == 404
    assert response.json() == {"error": "NotFound", "message": "Project 99 not found"}


def test_admin_can_read_any_project(client, ana_project, admin_headers):
    assert client.get("/projects/1", headers=admin_headers).status_code == 200


def test_patch_project_only_changes_sent_fields(client, ana_project, ana_headers):
    response = client.patch("/projects/1", json={"name": "Thesis v2"}, headers=ana_headers)
    assert response.json()["name"] == "Thesis v2"
    assert response.json()["description"] == "Final year"


def test_patch_project_by_other_user_or_admin_is_403(client, ana_project, ben_headers, admin_headers):
    assert client.patch("/projects/1", json={"name": "Mine now"}, headers=ben_headers).status_code == 403
    assert client.patch("/projects/1", json={"name": "Admin edit"}, headers=admin_headers).status_code == 403


def test_delete_project_also_deletes_its_tasks(client, ana_project, ana_headers):
    client.post("/projects/1/tasks", json={"title": "Intro"}, headers=ana_headers)
    assert client.delete("/projects/1", headers=ana_headers).status_code == 204
    assert client.get("/projects/1", headers=ana_headers).status_code == 404
    assert client.get("/tasks", headers=ana_headers).json() == []


def test_delete_project_other_user_403_admin_204(client, ana_project, ben_headers, admin_headers):
    assert client.delete("/projects/1", headers=ben_headers).status_code == 403
    assert client.delete("/projects/1", headers=admin_headers).status_code == 204


def test_project_tasks_list_and_access(client, ana_project, ana_headers, ben_headers, admin_headers):
    client.post("/projects/1/tasks", json={"title": "Intro"}, headers=ana_headers)
    assert len(client.get("/projects/1/tasks", headers=ana_headers).json()) == 1
    assert len(client.get("/projects/1/tasks", headers=admin_headers).json()) == 1
    assert client.get("/projects/1/tasks", headers=ben_headers).status_code == 403


def test_only_the_owner_can_add_tasks(client, ana_project, ben_headers):
    assert client.post("/projects/1/tasks", json={"title": "Sneaky"}, headers=ben_headers).status_code == 403
    assert client.post("/projects/99/tasks", json={"title": "Lost"}, headers=ben_headers).status_code == 404
