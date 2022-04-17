"""
    TODOS: functional tests.
"""


def test_todos_without_auth(test_client):
    """ Testing todos without auth. """

    response = test_client.get("/v1/todos",
                                follow_redirects=True)

    assert response.status_code == 401
    assert response.json["error"]["reason"] == "Unauthorized. You supplied the wrong credentials! Expecting a Bearer Token."


def test_successful_get_todos(btoken, test_client):
    """ Testing todos. """

    response = test_client.get("/v1/todos",
                                headers={ "Authorization": btoken },
                                follow_redirects=True)

    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert isinstance(response.json[0], dict)
    assert "id" in response.json[0]
    assert "title" in response.json[0]
    assert len(response.json) == 5


def test_successful_get_todos_limited(btoken, test_client):
    """ Testing todos limited by 1. """

    response = test_client.get("/v1/todos?limit=1",
                                headers={ "Authorization": btoken },
                                follow_redirects=True)

    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert isinstance(response.json[0], dict)
    assert "id" in response.json[0]
    assert "title" in response.json[0]
    assert len(response.json) == 1
