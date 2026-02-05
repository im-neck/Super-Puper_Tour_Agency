def test_register_and_login(client, unique_email):
    register_payload = {
        "email": unique_email,
        "password": "12345678",
        "full_name": "Eva Shalimova",
        "phone": "123456789",
    }
    response = client.post("/api/auth/register", json=register_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == unique_email

    login_data = {
        "username": unique_email,
        "password": "12345678",
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"
