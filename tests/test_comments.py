def test_create_comment(
    authorized_client,
    workspace,
    task,
):
    response = authorized_client.post(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/comments",
        json={
            "content": "First comment",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["content"] == "First comment"
    assert data["task_id"] == task["id"]
    
def test_get_comments(
    authorized_client,
    workspace,
    comment,
    task,
):
    response = authorized_client.get(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/comments"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["content"] == "First comment"
    
def test_create_comment_without_content(
    authorized_client,
    workspace,
    task,
):
    response = authorized_client.post(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/comments",
        json={},
    )

    assert response.status_code == 422
    
def test_create_comment_invalid_task(
    authorized_client,
    workspace,
):
    response = authorized_client.post(
        f"/workspaces/{workspace['id']}/tasks/999/comments",
        json={
            "content": "Comment",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
    
def test_create_comment_invalid_workspace(
    authorized_client,
):
    response = authorized_client.post(
        "/workspaces/999/tasks/1/comments",
        json={
            "content": "Comment",
        },
    )

    assert response.status_code == 404
    
def test_update_comment(
    authorized_client,
    workspace,
    comment,
):
    response = authorized_client.patch(
        f"/workspaces/{workspace['id']}/comments/{comment['id']}",
        json={
            "content": "Updated comment",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["content"] == "Updated comment"
    
def test_update_non_existing_comment(
    authorized_client,
    workspace,
):
    response = authorized_client.patch(
        f"/workspaces/{workspace['id']}/comments/999",
        json={
            "content": "Updated",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Comment not found"
    
def test_delete_comment(
    authorized_client,
    workspace,
    comment,
):
    response = authorized_client.delete(
        f"/workspaces/{workspace['id']}/comments/{comment['id']}"
    )

    assert response.status_code == 204
    
def test_delete_non_existing_comment(
    authorized_client,
    workspace,
):
    response = authorized_client.delete(
        f"/workspaces/{workspace['id']}/comments/999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Comment not found"
    
def test_member_cannot_update_other_comment(
    member_client,
    workspace,
    comment,
):
    response = member_client.patch(
        f"/workspaces/{workspace['id']}/comments/{comment['id']}",
        json={
            "content": "Hack",
        },
    )

    assert response.status_code == 403
    
def test_member_cannot_delete_other_comment(
    member_client,
    workspace,
    comment,
):
    response = member_client.delete(
        f"/workspaces/{workspace['id']}/comments/{comment['id']}"
    )

    assert response.status_code == 403
    
def test_non_member_cannot_get_comments(
    outsider_client,
    workspace,
    task,
):
    response = outsider_client.get(
        f"/workspaces/{workspace['id']}/tasks/{task['id']}/comments"
    )

    assert response.status_code == 403