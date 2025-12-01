# server/testing/conftest.py

import os
import sys
import pytest

# Ensure project root is on sys.path so "server" can be imported
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))      # server/testing
SERVER_DIR = os.path.dirname(CURRENT_DIR)                     # server
ROOT_DIR = os.path.dirname(SERVER_DIR)                        # project root

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from server.app import app
from server.models import db, Episode, Guest, Appearance


@pytest.fixture
def test_app():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def sample_data(test_app):
    """
    Create sample episodes, guests, appearances for API tests.
    Return ONLY IDs to avoid DetachedInstanceError (no detached models).
    """
    with test_app.app_context():
        ep1 = Episode(date="1/11/99", number=1)
        ep2 = Episode(date="1/12/99", number=2)

        g1 = Guest(name="Michael J. Fox", occupation="actor")
        g2 = Guest(name="Sandra Bernhard", occupation="Comedian")
        g3 = Guest(name="Tracey Ullman", occupation="television actress")

        db.session.add_all([ep1, ep2, g1, g2, g3])
        db.session.commit()

        a1 = Appearance(rating=4, episode_id=ep1.id, guest_id=g1.id)
        a2 = Appearance(rating=5, episode_id=ep2.id, guest_id=g2.id)
        db.session.add_all([a1, a2])
        db.session.commit()

        # Return only primitive data (IDs), not model instances
        return {
            "ep1_id": ep1.id,
            "ep2_id": ep2.id,
            "g1_id": g1.id,
            "g2_id": g2.id,
            "g3_id": g3.id,
        }
