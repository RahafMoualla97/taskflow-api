from app.constants.roles import WorkspaceRole

def test_add_member(workspace_member):
    assert workspace_member["role"] == "MEMBER"
    
    
def test_add_duplicate_member(
    authorized_client,
    workspace,
    member_user,
    workspace_member,
):
    response = authorized_client.post(
        f"/workspaces/{workspace['id']}/members",
        json={
            "user_id": member_user["user"]["id"],
            "role": WorkspaceRole.MEMBER.value,
        },
    )
    print(response.json())
    assert response.status_code == 400