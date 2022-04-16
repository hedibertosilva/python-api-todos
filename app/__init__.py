"""
    App Factory
        The main script responsible for creating a new
        instances of the application.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from sqlalchemy import exc

from app.extensions.handlers import handle_error


db = SQLAlchemy()


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
            new_user = User("admin", "admin")
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
