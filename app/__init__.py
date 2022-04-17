"""
    App Factory
        The main script responsible for creating a new
        instances of the application.
"""
import os
import logging
from flask import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.testing import FlaskClient
from werkzeug.exceptions import HTTPException
from sqlalchemy import exc

from app.extensions.handlers import handle_error


db = SQLAlchemy()

DEFAULT_ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
DEFAULT_ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")


logging.basicConfig(level='DEBUG')


class TestClient(FlaskClient):
    """ Manage test client request to dumps json field into data. """
    def open(self, *args, **kwargs):
        if "json" in kwargs:
            kwargs["data"] = json.dumps(kwargs.pop("json"))
            kwargs["content_type"] = "application/json"
        return super(TestClient, self).open(*args, **kwargs)


def create_app(config: str) -> Flask:
    """ Creates a new instance from app.

    Loads the initial environment configurations using the pyconfig
    file on instance parent path. It also initializer the extensions
    and register all blueprints routes.

    Args:
        config (str): Filename.

    Returns:
        Flask: Returns a Flask instance.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config)
    app.test_client_class = TestClient
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app: Flask) -> None:
    """ Initializer all extensions and register error handlers.

    By default, the system will register the first: <User: admin>"

    Args:
        app (Flask): Instance configured.
    """
    from app.models.user import User

    with app.app_context():
        db.init_app(app)
        db.create_all()
        try:
            new_user = User(DEFAULT_ADMIN_USER, DEFAULT_ADMIN_PASSWORD)
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
        app.register_error_handler(HTTPException, handle_error)


def register_blueprints(app: Flask) -> None:
    """ Registering all the routes.

    Args:
        app (Flask): Instance configured.
    """
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.todos import todos_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(todos_bp)
