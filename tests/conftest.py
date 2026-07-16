import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_db
from app.constants.roles import WorkspaceRole


TEST_DATABASE_URL = (
    "postgresql://taskflow_user:taskflow123@localhost:5432/taskflow_test_db"
)

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@pytest.fixture()
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
    
    
@pytest.fixture()
def user(client):
    response = client.post(
        "/users",
        json={
            "email": "owner@test.com",
            "username": "owner",
            "password": "12345678",
        },
    )

    return response.json()

@pytest.fixture()
def registered_user(client):
    response = client.post(
        "/users",
        json={
            "email": "owner@test.com",
            "username": "owner",
            "password": "12345678",
        },
    )
    print("REGISTERED:", response.json())
    assert response.status_code == 201

    return {
        "email": "owner@test.com",
        "username": "owner",
        "password": "12345678",
        "user": response.json(),
    }
    
    
@pytest.fixture()
def access_token(client, registered_user):
    response = client.post(
        "/auth/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    print("OWNER TOKEN:", response.json()["access_token"])
    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture()
def authorized_client(db_session, access_token):
    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as client:
        client.headers["Authorization"] = f"Bearer {access_token}"
        yield client

    app.dependency_overrides.clear()



@pytest.fixture()
def workspace(authorized_client):

    response = authorized_client.post(
        "/workspaces",
        json={
            "name": "Test Workspace"
        },
    )
    print(response.json()) 

    assert response.status_code == 201


    return response.json()

@pytest.fixture()
def member_user(client):
    response = client.post(
        "/users",
        json={
            "email": "member@test.com",
            "username": "member",
            "password": "12345678",
        },
    )
    print("MEMBER:", response.json())
    assert response.status_code == 201

    return {
        "email": "member@test.com",
        "username": "member",
        "password": "12345678",
        "user": response.json(),
    }
    
@pytest.fixture()
def workspace_member(
    authorized_client,
    workspace,
    member_user,
):
    response = authorized_client.post(
        f"/workspaces/{workspace['id']}/members",
        json={
            "user_id": member_user["user"]["id"],
            "role": WorkspaceRole.MEMBER.value,
        },
    )
    print(response.json())
    assert response.status_code == 201

    return response.json()

@pytest.fixture()
def task(
    authorized_client,
    workspace,
):
    response = authorized_client.post(
        f"/workspaces/{workspace['id']}/tasks",
        json={
            "title": "First Task",
            "description": "My first task",
            "priority": "medium",
        },
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture()
def member_access_token(client, member_user):
    response = client.post(
        "/auth/login",
        data={
            "username": member_user["email"],
            "password": member_user["password"],
        },
    )
    print("MEMBER TOKEN:", response.json()["access_token"])

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture()
def member_client(db_session, member_access_token):
    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as client:
        client.headers["Authorization"] = f"Bearer {member_access_token}"
        yield client

    app.dependency_overrides.clear()
    
    
@pytest.fixture()
def comment(
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

    return response.json()

@pytest.fixture()
def outsider_user(client):
    response = client.post(
        "/users",
        json={
            "email": "outsider@test.com",
            "username": "outsider",
            "password": "12345678",
        },
    )

    assert response.status_code == 201

    return {
        "email": "outsider@test.com",
        "username": "outsider",
        "password": "12345678",
        "user": response.json(),
    }
    
@pytest.fixture()
def outsider_access_token(
    client,
    outsider_user,
):
    response = client.post(
        "/auth/login",
        data={
            "username": outsider_user["email"],
            "password": outsider_user["password"],
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]

@pytest.fixture()
def outsider_client(
    db_session,
    outsider_access_token,
):
    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as client:
        client.headers["Authorization"] = (
            f"Bearer {outsider_access_token}"
        )
        yield client

    app.dependency_overrides.clear()