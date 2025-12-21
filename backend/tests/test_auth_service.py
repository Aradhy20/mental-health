import pytest
from fastapi.testclient import TestClient
from auth_service.main import app
from shared.models import User
from shared.auth import get_password_hash

client = TestClient(app)

def test_register_user(db_session, override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "user_id" in data

def test_login_user(db_session, override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    
    # Create user first
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        name="Test User"
    )
    db_session.add(user)
    db_session.commit()
    
    response = client.post(
        "/auth/token",
        data={
            "username": "testuser",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
