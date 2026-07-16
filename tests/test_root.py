
def test_root(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "TaskFlow API"
    assert data["status"] == "running"
    assert data["version"] == "1.0"