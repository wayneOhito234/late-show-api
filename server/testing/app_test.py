# server/testing/app_test.py

def test_index_route(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Late Show API is running"


def test_get_episodes(client, sample_data):
    resp = client.get("/episodes")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert {"id", "date", "number"} <= set(data[0].keys())


def test_get_episode_by_id_success(client, sample_data):
    ep1_id = sample_data["ep1_id"]

    resp = client.get(f"/episodes/{ep1_id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == ep1_id
    assert "appearances" in data
    assert isinstance(data["appearances"], list)


def test_get_episode_by_id_not_found(client):
    resp = client.get("/episodes/9999")
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "Episode not found"}


def test_delete_episode_success(client, sample_data):
    ep1_id = sample_data["ep1_id"]

    resp = client.delete(f"/episodes/{ep1_id}")
    assert resp.status_code == 204
    assert resp.data == b""  # empty body


def test_delete_episode_not_found(client):
    resp = client.delete("/episodes/9999")
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "Episode not found"}


def test_get_guests(client, sample_data):
    resp = client.get("/guests")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert {"id", "name", "occupation"} <= set(data[0].keys())


def test_post_appearance_success(client, sample_data):
    ep2_id = sample_data["ep2_id"]
    g3_id = sample_data["g3_id"]

    resp = client.post(
        "/appearances",
        json={"rating": 5, "episode_id": ep2_id, "guest_id": g3_id},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["rating"] == 5
    assert data["episode"]["id"] == ep2_id
    assert data["guest"]["id"] == g3_id


def test_post_appearance_validation_error_bad_rating(client, sample_data):
    ep2_id = sample_data["ep2_id"]
    g3_id = sample_data["g3_id"]

    resp = client.post(
        "/appearances",
        json={"rating": 10, "episode_id": ep2_id, "guest_id": g3_id},
    )
    assert resp.status_code == 400
    data = resp.get_json()
    assert "errors" in data


def test_post_appearance_validation_error_missing_fields(client):
    # missing guest_id
    resp = client.post(
        "/appearances",
        json={"rating": 3, "episode_id": 1},
    )
    assert resp.status_code == 400
    data = resp.get_json()
    assert "errors" in data
