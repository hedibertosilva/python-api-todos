"""
    Setup configurations.
"""
from setuptools import setup


setup(
    name="python-api-todos",
      version="1.0",
      description="Proxy to 3rd party data.",
      author="Hediberto C. Silva",
      author_username="hed.cavalcante@gmail.com",
      packages=["app"],
      zip_safe=False,
      install_requires=[
          "PyJWT==1.4.*",
          "requests==2.27.*",
          "python-dotenv==0.20.*",
          "Flask==2.1.1",
          "gunicorn==20.1.*",
          "Flask-SQLAlchemy==2.5.*",
          "tox==3.25.*"
      ],
      extras_require={
          "test": [
              "coverage",
              "pytest",
              "mypy",
              "flake8"
          ]
      }
)
