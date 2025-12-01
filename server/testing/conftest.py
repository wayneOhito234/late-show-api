# server/testing/conftest.py

import pytest
from server.app import app, db
from server.models import Episode, Guest, Appearance


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

        return {"ep1": ep1, "ep2": ep2, "g1": g1, "g2": g2, "g3": g3}
