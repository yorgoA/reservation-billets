import pytest
import requests

BASE_URL = "http://app:8080"

@pytest.fixture(scope="module", autouse=True)
def setup():
    # Setup actions (if any) before running tests
    yield
    # Teardown actions (if any) after running tests

def test_home():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.text == "Hello, World!"

def test_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_etcd():
    response = requests.get(f"{BASE_URL}/etcd-test")
    assert response.status_code == 200
    assert response.text == "test_value"

def test_events():
    response = requests.get(f"{BASE_URL}/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_reserve():
    data = {
        "event_id": 1,
        "user_id": 1,
        "num_tickets": 2
    }
    response = requests.post(f"{BASE_URL}/reserve", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Reservation successful"

def test_reservations():
    response = requests.get(f"{BASE_URL}/reservations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
