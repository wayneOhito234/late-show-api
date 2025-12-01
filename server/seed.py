# server/seed.py

from server.app import app
from server.models import db, Episode, Guest, Appearance


def seed_data():
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()

        print("Creating tables...")
        db.create_all()

        # ---- EPISODES ----
        ep1 = Episode(date="1/11/99", number=1)
        ep2 = Episode(date="1/12/99", number=2)

        # ---- GUESTS ----
        g1 = Guest(name="Michael J. Fox", occupation="actor")
        g2 = Guest(name="Sandra Bernhard", occupation="Comedian")
        g3 = Guest(name="Tracey Ullman", occupation="television actress")

        db.session.add_all([ep1, ep2, g1, g2, g3])
        db.session.commit()

        # ---- APPEARANCES ----
        a1 = Appearance(rating=4, episode_id=ep1.id, guest_id=g1.id)
        a2 = Appearance(rating=5, episode_id=ep2.id, guest_id=g2.id)
        a3 = Appearance(rating=5, episode_id=ep2.id, guest_id=g3.id)

        db.session.add_all([a1, a2, a3])
        db.session.commit()

        print("✔ Database successfully seeded!")
        print("Episodes:", Episode.query.count())
        print("Guests:", Guest.query.count())
        print("Appearances:", Appearance.query.count())


if __name__ == "__main__":
    seed_data()
