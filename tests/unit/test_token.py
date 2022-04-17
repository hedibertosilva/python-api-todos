"""
    TOKEN: unit tests.
"""
import time
import pytest
from datetime import datetime
from secrets import token_urlsafe

from app.libs.token import Token

secret_key = token_urlsafe(32)


def test_encoding_and_decoding_token():
    """ Testing encode and decode token. """
    i_token = Token(secret_key)
    i_token.encoding(user_id=10)
    btoken = i_token.bearer_token
    token_data = i_token.decoding(btoken)

    assert isinstance(token_data, dict)
    assert token_data["id"] == 10
    assert isinstance(token_data["expires_at"], str)

@pytest.mark.parametrize("btoken,result", [
    ["Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9", True],
    ["eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9", False]
])
def test_method_is_bearer_token(btoken, result):
    """ Testing classmethod is_bearer. """
    assert Token.is_bearer(btoken) == result

def test_token_expiration_time():
    """ Testing calculate to expiration time. """
    i_token = Token(secret_key, token_timedelta=2)
    i_token.encoding(user_id=10)
    btoken = i_token.bearer_token
    token_data = i_token.decoding(btoken)

    time.sleep(2)
    now = datetime.utcnow()
    date = datetime.strptime(token_data["expires_at"], "%Y-%m-%d %H:%M:%S.%f")

    assert date < now
