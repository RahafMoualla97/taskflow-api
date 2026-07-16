def test_create_task(
    authorized_client,
    workspace,
):
    response = authorized_client.post(
        f"/workspaces/{workspace['id']}/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "Study testing",
            "priority": "high",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Study testing"
    assert data["priority"] == "high"
    assert data["workspace_id"] == workspace["id"]
    

def test_get_workspace_tasks(
    authorized_client,
    workspace,
    task,
):
    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1

    assert data["items"][0]["title"] == "First Task"
    
    
def test_create_task_without_title(
    authorized_client,
    workspace,
):
    response = authorized_client.post(
        f"/workspaces/{workspace['id']}/tasks",
        json={
            "description": "No title",
        },
    )

    assert response.status_code == 422
    
    
def test_create_task_invalid_workspace(
    authorized_client,
):
    response = authorized_client.post(
        "/workspaces/999/tasks",
        json={
            "title": "Task",
            "priority": "medium",
        },
    )

    assert response.status_code == 404
    
    
def test_update_task_title(
    authorized_client,
    workspace,
    task,
):
    response = authorized_client.patch(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}",
        json={
            "title": "Updated Task",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated Task"
    

def test_update_task_priority(
    authorized_client,
    workspace,
    task,
):
    response = authorized_client.patch(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}",
        json={
            "priority": "HIGH",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["priority"] == "HIGH"
    
def test_update_task_status(
    authorized_client,
    workspace,
    task,
):
    response = authorized_client.patch(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}",
        json={
            "status": "IN_PROGRESS",
        },
    )

    assert response.status_code == 200

    assert response.json()["status"] == "IN_PROGRESS"
    
def test_update_non_existing_task(
    authorized_client,
    workspace,
):
    response = authorized_client.patch(
        f"/workspaces/{workspace['id']}/tasks/999",
        json={
            "title": "Updated",
        },
    )

    assert response.status_code == 404
    
    
def test_delete_task(
    authorized_client,
    workspace,
    task,
):
    response = authorized_client.delete(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}"
    )

    assert response.status_code == 204
    
    
def test_deleted_task_not_in_list(
    authorized_client,
    workspace,
    task,
):
    authorized_client.delete(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}"
    )

    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 0
    assert len(data["items"]) == 0
    
    
def test_restore_task(
    authorized_client,
    workspace,
    task,
):
    authorized_client.delete(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}"
    )

    response = authorized_client.patch(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/restore"
    )

    assert response.status_code == 200

    assert response.json()["id"] == task["id"]
    
    
def test_restored_task_visible_again(
    authorized_client,
    workspace,
    task,
):
    authorized_client.delete(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}"
    )

    authorized_client.patch(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/restore"
    )

    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    
    
def test_restore_non_deleted_task(
    authorized_client,
    workspace,
    task,
):
    response = authorized_client.patch(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/restore"
    )

    assert response.status_code == 400
    
    
def test_delete_non_existing_task(
    authorized_client,
    workspace,
):
    response = authorized_client.delete(
        f"/workspaces/{workspace['id']}/tasks/999"
    )

    assert response.status_code == 404
    

def test_task_activity_after_create(
    authorized_client,
    workspace,
    task,
):
    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/logs"
    )

    assert response.status_code == 200

    logs = response.json()
    print(logs)

    assert len(logs) == 1
    assert logs[0]["action"] == "TASK_CREATED"
    
    
def test_task_activity_after_update(
    authorized_client,
    workspace,
    task,
):
    authorized_client.patch(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}",
        json={
            "title": "Updated Title",
        },
    )

    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/logs"
    )

    assert response.status_code == 200

    logs = response.json()
    print(logs)

    assert len(logs) == 2

    actions = [log["action"] for log in logs]

    assert "TASK_CREATED" in actions
    assert "TITLE_CHANGED" in actions
    
    
def test_task_activity_after_delete(
    authorized_client,
    workspace,
    task,
):
    authorized_client.delete(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}"
    )

    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/logs"
    )

    logs = response.json()
    print(response.json())
    
    assert len(logs) == 2
    actions = [log["action"] for log in logs]

    assert "TASK_CREATED" in actions
    assert "TASK_DELETED" in actions
    
    
def test_task_activity_after_restore(
    authorized_client,
    workspace,
    task,
):
    authorized_client.delete(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}"
    )

    authorized_client.patch(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/restore"
    )

    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/logs"
    )

    logs = response.json()

    assert len(logs) == 3
    actions = [log["action"] for log in logs]

    assert "TASK_CREATED" in actions
    assert "TASK_DELETED" in actions
    assert "TASK_RESTORED" in actions
    
    
def test_member_cannot_delete_task(
    member_client,
    workspace,
    task,
):
    print(member_client.get("/users/me").json())
    response = member_client.delete(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}"
    )

    assert response.status_code == 403
    

def test_member_cannot_restore_task(
    member_client,
    workspace,
    task,
):
    response = member_client.patch(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/restore"
    )

    assert response.status_code == 403
    
    
def test_get_task(
    authorized_client,
    workspace,
    task,
):
    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task["id"]
    assert data["title"] == task["title"]
    
def test_get_non_existing_task(
    authorized_client,
    workspace,
):
    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks/999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
    
    

def test_get_task_invalid_workspace(
    authorized_client,
):
    response = authorized_client.get(
        "/workspaces/999/tasks/1"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Workspace not found"
    
def test_member_cannot_get_task(
    member_client,
    workspace,
    task,
):
    response = member_client.get(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}"
    )

    assert response.status_code == 403
    
def test_deleted_task_cannot_be_retrieved(
    authorized_client,
    workspace,
    task,
):
    authorized_client.delete(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}"
    )

    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"