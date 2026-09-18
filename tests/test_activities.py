from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def reset_activities():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["alice@mergington.edu"],
            },
            "Gym Class": {
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["bob@mergington.edu"],
            },
        }
    )


def test_get_activities_returns_activity_data():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"] == ["alice@mergington.edu"]


def test_signup_for_activity_adds_participant():
    # Arrange
    reset_activities()
    email = "charlie@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]
    assert response.json()["message"] == f"Signed up {email} for Chess Club"


def test_signup_duplicate_email_is_rejected():
    # Arrange
    reset_activities()
    email = "alice@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_them_from_activity():
    # Arrange
    reset_activities()
    email = "alice@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/participants?email=" + email)

    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"


def test_unregister_missing_participant_returns_404():
    # Arrange
    reset_activities()
    email = "not-here@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/participants?email=" + email)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
