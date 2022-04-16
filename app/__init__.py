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
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config)
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
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


def register_blueprints(app):
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.todos import todos_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(todos_bp)
