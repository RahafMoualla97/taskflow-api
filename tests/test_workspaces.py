def test_create_workspace(authorized_client):

    response = authorized_client.post(
        "/workspaces",
        json={
            "name": "My Workspace"
        },
    )


    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "My Workspace"
    
    
def test_get_workspaces(
    authorized_client,
    workspace
):

    response = authorized_client.get(
        "/workspaces"
    )


    assert response.status_code == 200