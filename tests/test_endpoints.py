from urllib.parse import quote

import src.app as app_module


def test_get_activities_returns_activity_catalog(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert expected_activity in payload
    assert payload[expected_activity]["description"] == app_module.activities[expected_activity]["description"]
    assert isinstance(payload[expected_activity]["participants"], list)


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (307, 308)
    assert response.headers["location"] == expected_location


def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    original_count = len(app_module.activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]
    assert len(app_module.activities[activity_name]["participants"]) == original_count + 1


def test_unregister_removes_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original_count = len(app_module.activities[activity_name]["participants"])

    # Act
    response = client.delete(f"/activities/{quote(activity_name)}/participants?email={quote(email)}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]
    assert len(app_module.activities[activity_name]["participants"]) == original_count - 1