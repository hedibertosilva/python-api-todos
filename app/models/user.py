"""
    Provides a user model
"""
from datetime import datetime
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app import db


class User(db.Model):
    """ Represents User.

        Attributes:
            id (int): Sequential integer number.
            username (str): Username address of the user.
            password (str): Hashed password (using werkzeug.security).
            created_at (Datetime) - Datime that user was created.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, username: str, password: str):
        """ Create a new User object using the username address and hashing the
            plaintext password using Werkzeug.Security.
        """
        self.username = username
        self.password = self._generate_password_hash(password)
        self.created_at = datetime.now()

    def is_password_correct(self, password: str) -> bool:
        """ Verifying if the plaintext passoword supplied is correct.

        Args:
            password (str): Plaintext password

        Returns:
            bool: Returns True if the password supplied is corrent.
        """
        return check_password_hash(self.password, password)

    @staticmethod
    def _generate_password_hash(password: str) -> str:
        """ Generating hashed password using werkzeug.security.

        Args:
            password (str): Plaintext password.

        Returns:
            str: Hashed password.
        """
        return generate_password_hash(password)

    def save(self) -> None:
        """ Saving state of current user. """
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        """ Returning the user presentation. """
        return f"<User: {self.username}>"
