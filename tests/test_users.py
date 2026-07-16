def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "email": "owner@test.com",
            "username": "owner",
            "password": "12345678",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "owner@test.com"
    assert data["username"] == "owner"
    assert data["is_active"] is True
    assert data["is_superuser"] is False
    
    
def test_create_user_duplicate_email(client):
    user_data = {
        "email": "test@test.com",
        "username": "user1",
        "password": "12345678",
    }

    response = client.post(
        "/users",
        json=user_data,
    )

    assert response.status_code == 201


    response = client.post(
        "/users",
        json={
            "email": "test@test.com",
            "username": "user2",
            "password": "12345678",
        },
    )

    assert response.status_code == 400
    
def test_create_user_duplicate_username(client):

    response = client.post(
        "/users",
        json={
            "email": "user1@test.com",
            "username": "same_username",
            "password": "12345678",
        },
    )

    assert response.status_code == 201


    response = client.post(
        "/users",
        json={
            "email": "user2@test.com",
            "username": "same_username",
            "password": "12345678",
        },
    )


    assert response.status_code == 400