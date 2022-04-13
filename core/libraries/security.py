"""
    Security Model
"""
from hmac import compare_digest
from core.models.user import User


__all__ = ["authenticate", "identity"]

_DEFAULT_ADMIN_USER = "admin"
_DEFAULT_ADMIN_PASSWORD = "admin"

users = [
    User(1, _DEFAULT_ADMIN_USER, _DEFAULT_ADMIN_PASSWORD)
]


def authenticate(username: str, password: str) -> User:
    user = User.find_by_username(username)
    if user and compare_digest(user.password, password):
        return user
    return None


def identity(payload: dict) -> User:
    try:
        user_id = int(payload["identity"])
        [user] = filter(lambda u: u.find_by_user_id(user_id), users)
    except ValueError:
        return None
    return user
