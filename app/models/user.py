"""
    User Model
"""
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
        Class that represents a user of the application.

        Attributes:
            id (int) - sequential integer number
            email (string) - email address of the user
            password (string) - hashed password (using werkzeug.security)
            created_at - created time
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, email: str, password: str):
        """
            Create a new User object using the email address and hashing the
            plaintext password using Werkzeug.Security.
        """
        self.email = email
        self.password = self._generate_password_hash(password)
        self.created_at = datetime.now()

    def is_password_correct(self, password: str):
        return check_password_hash(self.password, password)

    def set_password(self, password: str):
        self.password = self._generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def _generate_password_hash(password):
        return generate_password_hash(password)

    def __repr__(self):
        return f"<User: {self.email}>"

    @property
    def is_authenticated(self):
        """Return True if the user has been successfully registered."""
        return True

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren"t supported."""
        return False

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return self.id
