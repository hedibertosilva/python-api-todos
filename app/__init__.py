"""
    App Factory
        The main script responsible for creating a new
        instances of the application.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc


db = SQLAlchemy()


def create_app(config_filename: str) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)

    return app

def initialize_extensions(app):
    from app.models.user import User

    db.init_app(app)
    with app.app_context():
        db.create_all()
        try:
            new_user = User('admin', 'admin')
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()


def register_blueprints(app):
    from app.routes.auth import auth_blueprint
    from app.routes.todos import todos_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(todos_blueprint)
