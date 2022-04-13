"""
    Provides method to initialize a new instance with JWT security.
"""
from flask import Flask
from flask_jwt import JWT
from app.libraries.security import authenticate, identity
from app.routes import app


__all__ = ["create_app", "initialize_security"]


def create_app(config_filename: str) -> Flask:
    app.config.from_pyfile(config_filename)
    initialize_security(app)
    return app


def initialize_security(app: Flask) -> None:
    JWT(app, authenticate, identity)
