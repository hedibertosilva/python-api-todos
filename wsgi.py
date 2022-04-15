#!/usr/bin/env python3
"""
    Web Server Gateway Interface (WSGI).
"""
import argparse
from app import create_app


# Choosing Environmental Configs.
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-e",
                        action="store",
                        type=str,
                        default="production",
                        choices=["production", "testing"],
                        help="Choise from production or testing.")
args = arg_parser.parse_args()

# Creating a new app instance.
filename = f"{args.e}.cfg"
app = create_app(filename)


if __name__ == "__main__":
    raise SystemExit(app.run())
