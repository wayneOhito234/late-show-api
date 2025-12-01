# server/testing/models_test.py

import pytest
from server.app import db
from server.models import Episode, Guest, Appearance


def test_episode_guest_relationship(test_app):
    with test_app.app_context():
        ep = Episode(date="1/11/99", number=1)
        g = Guest(name="Test Guest", occupation="tester")
        db.session.add_all([ep, g])
        db.session.commit()

        a = Appearance(rating=4, episode_id=ep.id, guest_id=g.id)
        db.session.add(a)
        db.session.commit()

        assert len(ep.appearances) == 1
        assert ep.appearances[0].guest is g
        assert g.appearances[0].episode is ep


def test_rating_validation(test_app):
    with test_app.app_context():
        ep = Episode(date="1/11/99", number=1)
        g = Guest(name="Test Guest", occupation="tester")
        db.session.add_all([ep, g])
        db.session.commit()

        # Valid rating
        a = Appearance(rating=5, episode_id=ep.id, guest_id=g.id)
        db.session.add(a)
        db.session.commit()

        # Invalid rating should raise
        with pytest.raises(ValueError):
            Appearance(rating=10, episode_id=ep.id, guest_id=g.id)


def test_cascade_delete(test_app):
    with test_app.app_context():
        ep = Episode(date="1/11/99", number=1)
        g = Guest(name="Test Guest", occupation="tester")
        db.session.add_all([ep, g])
        db.session.commit()

        a = Appearance(rating=4, episode_id=ep.id, guest_id=g.id)
        db.session.add(a)
        db.session.commit()

        assert Appearance.query.count() == 1
        db.session.delete(ep)
        db.session.commit()
        assert Appearance.query.count() == 0
