"""
    AUTH: functional tests.
"""
from app import DEFAULT_ADMIN_USER
from app import DEFAULT_ADMIN_PASSWORD
from app.libs.token import Token


def test_successful_login(test_client):
    """ Testing to login. """
    response = test_client.post("/v1/login",
                                json={
                                    "username": DEFAULT_ADMIN_USER,
                                    "password": DEFAULT_ADMIN_PASSWORD
                                },
                                follow_redirects=True)

    assert response.status_code == 201
    assert "data" in response.json
    assert "message" in response.json
    assert "expires_at" in response.json["data"]
    assert "token" in response.json["data"]
    assert "user" in response.json["data"]
    assert isinstance(response.json["data"]["user"], dict)
    assert "id" in response.json["data"]["user"]
    assert "created_at" in response.json["data"]["user"]
    assert response.json["message"] == "The token was generated successfully."
    assert Token.is_bearer(response.json["data"]["token"])


def test_login_without_body(test_client):
    """ Testing login without body. """

    response = test_client.post("/v1/login",
                                follow_redirects=True)

    assert response.status_code == 400
    assert "Bad Request." in response.json["error"]["reason"]


def test_login_without_user_or_password(test_client):
    """ Testing user registration without user or password. """

    response = test_client.post("/v1/login",
                                json={},
                                follow_redirects=True)

    assert response.status_code == 400
    assert response.json["error"]["reason"] == "Bad Request. Please, supply the credentials required."
