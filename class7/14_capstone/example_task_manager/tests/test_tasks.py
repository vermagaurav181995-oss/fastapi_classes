import pytest


@pytest.fixture
def ana_tasks(client, ana_headers) -> list[dict]:
    client.post("/projects", json={"name": "Thesis"}, headers=ana_headers)
    client.post("/projects", json={"name": "Home"}, headers=ana_headers)
    payloads = [
        (1, {"title": "Write intro", "due_date": "2026-12-01"}),
        (1, {"title": "Write chapter 1", "status": "in_progress", "due_date": "2026-12-15"}),
        (1, {"title": "Pick a title", "status": "done", "due_date": "2026-11-20"}),
        (2, {"title": "Fix the sink"}),
    ]
    return [client.post(f"/projects/{pid}/tasks", json=body, headers=ana_headers).json() for pid, body in payloads]


def titles(response) -> list[str]:
    return [task["title"] for task in response.json()]


def test_task_defaults(client, ana_tasks):
    assert ana_tasks[3] == {
        "id": 4, "project_id": 2, "title": "Fix the sink", "description": "",
        "status": "todo", "due_date": None, "owner_id": 2,
    }


def test_list_sorted_by_due_date_with_no_date_last(client, ana_tasks, ana_headers):
    assert titles(client.get("/tasks", headers=ana_headers)) == [
        "Pick a title", "Write intro", "Write chapter 1", "Fix the sink",
    ]


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("status=todo", ["Write intro", "Fix the sink"]),
        ("status=in_progress", ["Write chapter 1"]),
        ("status=done", ["Pick a title"]),
        ("due_before=2026-12-01", ["Pick a title", "Write intro"]),
        ("due_after=2026-12-01", ["Write intro", "Write chapter 1"]),
        ("due_after=2026-11-25&due_before=2026-12-10", ["Write intro"]),
        ("project_id=2", ["Fix the sink"]),
        ("status=todo&project_id=1", ["Write intro"]),
        ("skip=1&limit=2", ["Write intro", "Write chapter 1"]),
    ],
)
def test_task_filters(client, ana_tasks, ana_headers, query, expected):
    assert titles(client.get(f"/tasks?{query}", headers=ana_headers)) == expected


@pytest.mark.parametrize("query", ["status=later", "due_before=tomorrow", "limit=0", "skip=-1"])
def test_invalid_filters_return_422(client, ana_headers, query):
    assert client.get(f"/tasks?{query}", headers=ana_headers).status_code == 422


def test_users_do_not_see_other_users_tasks(client, ana_tasks, ben_headers, admin_headers):
    assert client.get("/tasks", headers=ben_headers).json() == []
    assert len(client.get("/tasks", headers=admin_headers).json()) == 4


def test_get_task_owner_other_admin_missing(client, ana_tasks, ana_headers, ben_headers, admin_headers):
    assert client.get("/tasks/1", headers=ana_headers).status_code == 200
    assert client.get("/tasks/1", headers=ben_headers).status_code == 403
    assert client.get("/tasks/1", headers=admin_headers).status_code == 200
    assert client.get("/tasks/99", headers=ana_headers).json()["message"] == "Task 99 not found"


def test_patch_task_status_keeps_other_fields(client, ana_tasks, ana_headers):
    response = client.patch("/tasks/1", json={"status": "done"}, headers=ana_headers)
    assert response.json()["status"] == "done"
    assert response.json()["title"] == "Write intro" and response.json()["due_date"] == "2026-12-01"


def test_patch_task_by_other_user_is_403(client, ana_tasks, ben_headers):
    assert client.patch("/tasks/1", json={"status": "done"}, headers=ben_headers).status_code == 403


def test_patch_task_invalid_status_is_422(client, ana_tasks, ana_headers):
    assert client.patch("/tasks/1", json={"status": "someday"}, headers=ana_headers).status_code == 422


def test_delete_task_owner_and_admin(client, ana_tasks, ana_headers, ben_headers, admin_headers):
    assert client.delete("/tasks/1", headers=ben_headers).status_code == 403
    assert client.delete("/tasks/1", headers=ana_headers).status_code == 204
    assert client.delete("/tasks/2", headers=admin_headers).status_code == 204
    assert client.delete("/tasks/1", headers=ana_headers).status_code == 404


def test_tasks_require_login(client):
    assert client.get("/tasks").status_code == 401
