#!/usr/bin/env python3
"""
    Web Server Gateway Interface [WSGI]
"""
from app import app


if __name__ == '__main__':
    raise SystemExit(app.run())
