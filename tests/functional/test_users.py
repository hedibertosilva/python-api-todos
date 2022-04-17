"""
    USERS: functional tests.
"""
import string
import random

from app import DEFAULT_ADMIN_USER
from app import DEFAULT_ADMIN_PASSWORD


def test_successful_user_registration(test_client):
    """ Testing successful user registration. """

    random_username = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))

    response = test_client.post("/v1/users",
                                json={
                                    "username": random_username,
                                    "password": "password"
                                },
                                follow_redirects=True)

    assert response.status_code == 201
    assert "data" in response.json
    assert "created_at" in response.json["data"]
    assert "id" in response.json["data"]
    assert response.json["data"]["username"] == random_username
    assert "message" in response.json
    assert response.json["message"] == "The user has been successfully registered."


def test_user_registration_without_body(test_client):
    """ Testing user registration without body. """

    response = test_client.post("/v1/users",
                                follow_redirects=True)

    assert response.status_code == 400
    assert "Bad Request." in response.json["error"]["reason"]


def test_user_already_exists(test_client):
    """ Testing if users is already registered. """
    response = test_client.post("/v1/users",
                                json={
                                    "username": DEFAULT_ADMIN_USER,
                                    "password": DEFAULT_ADMIN_PASSWORD
                                },
                                follow_redirects=True)

    assert response.status_code == 202
    assert response.json["message"] == "User already exists."


def test_user_without_user_or_password(test_client):
    """ Testing user registration without user or password. """

    response = test_client.post("/v1/users",
                                json={},
                                follow_redirects=True)

    assert response.status_code == 400
    assert response.json["error"]["reason"] == "Bad Request. Please, supply the username and password data."
