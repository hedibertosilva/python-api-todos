#!/usr/bin/env python3
"""
    Web Server Gateway Interface (WSGI).
"""
from app import create_app


# Creating a new app instance for production env.
app = create_app("production.cfg")


if __name__ == "__main__":
    app.run()
