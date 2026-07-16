def test_access_token_fixture(access_token):
    assert access_token is not None
    assert isinstance(access_token, str)


def test_authorized_client(authorized_client):
    response = authorized_client.get("/users/me")

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "owner@test.com"
    assert data["username"] == "owner"
    
    
def test_login_wrong_password(client, registered_user):

    response = client.post(
        "/auth/login",
        data={
            "username": registered_user["email"],
            "password": "wrong_password",
        },
    )


    assert response.status_code == 401
    
    
def test_login_invalid_email(client):

    response = client.post(
        "/auth/login",
        data={
            "username": "fake@test.com",
            "password": "12345678",
        },
    )


    assert response.status_code == 401