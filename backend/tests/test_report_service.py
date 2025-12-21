import pytest
from fastapi.testclient import TestClient
from report_service.main import app
from shared.database import get_db

client = TestClient(app)

def test_calculate_wellness_score():
    response = client.post(
        "/wellness/calculate",
        json={
            "mood_score": 80,
            "sleep_quality": 75,
            "exercise_frequency": 60,
            "social_interaction": 50,
            "stress_level": 30
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "total_score" in data["score"]
    assert 0 <= data["score"]["total_score"] <= 100

def test_generate_goals(db_session, override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    
    response = client.post(
        "/goals/generate",
        json={
            "user_id": 1,
            "user_profile": {"name": "Test User"},
            "wellness_data": {"emotional_score": 60, "physical_score": 70},
            "therapy_notes": []
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "goals" in data
    assert len(data["goals"]) > 0
    assert "title" in data["goals"][0]
