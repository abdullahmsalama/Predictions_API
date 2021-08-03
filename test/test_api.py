"""
This file includes tests for the API
"""

from starlette.testclient import TestClient
from app.db import count_enteries_table

def test_health(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200

# Test that the prediction table were created sucessfully after the API startup 
def test_table_creation(client: TestClient):
    assert count_enteries_table() == 0

# Test that the prediction table was inserted to after a post call 
def test_table_insertion_after_post(client: TestClient):
    response = client.post(
        "/api/predict",
        json={"id": 1234, "recency_7": 1, "frequency_7": 1,\
         "monetary_7": 8.5},
    )
    assert count_enteries_table() == 1

def test_successful_post_call(client: TestClient):
    response = client.post(
        "/api/predict",
        json={"id": 1224, "recency_7": 1, "frequency_7": 1,\
         "monetary_7": 8.5},
    )

    assert response.status_code == 200

def test_fail_post_call(client: TestClient):
    response = client.post(
        "/api/predict",
        json={"id": "string", "recency_7": 2, "frequency_7": 1,\
         "monetary_7": 8.5},
    )
    """ Unprocessable entry because id has to be int, but got a
     string type """
    assert response.status_code == 422



def test_get_count_requests_unprocessable(client: TestClient):
    response = client.get(
        "/api/requests/'string'",
    )
    # Unprocessable entry because it wants to get a string type
    assert response.status_code == 422

def test_get_count_requests_newid(client: TestClient):
    response = client.get(
        "/api/requests/12345671234454898227654321",
    )
    assert response.status_code == 200


def test_get_count_after_post_requests(client: TestClient):
    # First, get request for an id that has not been seen before
    response = client.get(
        "/api/requests/1100",
    )
    # the count for this id should be 0 as it hasn't been seen before
    assert(response.json()['count']) == 0

    # Second, post request for this id "1100"
    client.post(
        "/api/predict",
        json={"id": 1100, "recency_7": 3, "frequency_7": 2,\
         "monetary_7": 3.5},
    )
    response = client.get(
        "/api/requests/1100",
    )

    # the count for this id should be 1 now
    assert(response.json()['count']) == 1

    # Third, another post request for this id "1100"
    client.post(
        "/api/predict",
        json={"id": 1100, "recency_7": 3, "frequency_7": 2,\
         "monetary_7": 3.5},
    )
    response = client.get(
        "/api/requests/1100",
    )

    # the count for this id should be 2 now
    assert(response.json()['count']) == 2

