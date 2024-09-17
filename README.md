# Orders-App
This is a simple customer and order management service created written in Python + Flask. The service has a database where data about customers and orders is uploaded using REST API.  When an order is uploaded, the customer receives an SMS alerting them.

## Libraries Used
- [Flask](http://flask.pocoo.org/), .
- [Flask-SQLAlchemy](https://pythonhosted.org/Flask-SQLAlchemy/) interacting with the database.
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) handles SQLAlchemy database migrations.
- [Flask-OpenID](https://pythonhosted.org/Flask-OpenID/) to add OpenID based authentication.
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)  adds support for quickly building REST APIs.
- [Requests](https://pypi.org/project/requests/) to send HTTP/1.1 requests.
- [Pytest](https://docs.pytest.org/en/stable/) to write small, readable tests.
- [pytest-cov](https://pypi.org/project/pytest-cov/) for measuring coverage.
- [Authlib](https://docs.authlib.org/en/latest/) for OpenID Connect.
