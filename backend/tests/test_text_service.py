import pytest
from fastapi.testclient import TestClient
from text_service.main import app
from shared.database import get_db

client = TestClient(app)

def test_analyze_text(db_session, override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    
    response = client.post(
        "/analyze/text",
        json={
            "text": "I feel really happy today because I accomplished my goals.",
            "user_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "emotion" in data
    assert "confidence" in data
    assert data["emotion"] in ["joy", "happy", "positive"]

def test_analyze_text_negative(db_session, override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    
    response = client.post(
        "/analyze/text",
        json={
            "text": "I am feeling very sad and lonely.",
            "user_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "emotion" in data
    assert data["emotion"] in ["sadness", "sad", "negative"]
