import os
import sys

import pytest
from app.models import User
from app import create_app

# Add the 'app' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


# can make client.get() and client.post() requests to the applications
@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user():
    user = User(name="test", email="email@test")
    user.save()
    yield user
