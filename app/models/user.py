"""
    Model
"""


class User(object):

    def __init__(self, user_id: int, username: str, password: str) -> None:
        self.user_id = user_id
        self.username = username
        self.password = password

    def find_by_username(self, username: str) -> bool:
        return self.username == username

    def find_by_user_id(self, user_id: int) -> bool:
        return self.user_id == user_id

    def __repr__(self) -> str:
        return f"User(id={self.user_id})"

    def __str__(self) -> str:
        return f"User(id={self.user_id})"
