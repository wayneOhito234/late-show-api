# server/app.py

import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource

from .models import db, Episode, Guest, Appearance  # relative import

app = Flask(__name__)

# ---- DB CONFIG: use a single, absolute DB path inside server/ ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # /.../late-show-api/server
DB_PATH = os.path.join(BASE_DIR, "app.db")                 # /.../late-show-api/server/app.db

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Make sure tables exist when the app starts
with app.app_context():
    db.create_all()


# ---------- ROUTES / RESOURCES ----------

class Index(Resource):
    def get(self):
        return {"message": "Late Show API is running"}, 200


# 1. GET /episodes
class Episodes(Resource):
    def get(self):
        episodes = Episode.query.all()
        # only id, date, number
        data = [
            {
                "id": e.id,
                "date": e.date,
                "number": e.number,
            }
            for e in episodes
        ]
        return data, 200


# 2 & 3. GET /episodes/<int:id>, DELETE /episodes/<int:id>
class EpisodeByID(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return {"error": "Episode not found"}, 404

        # Build JSON manually to avoid recursion & match spec
        ep_dict = {
            "id": episode.id,
            "date": episode.date,
            "number": episode.number,
            "appearances": [
                {
                    "id": a.id,
                    "rating": a.rating,
                    "guest_id": a.guest_id,
                    "episode_id": a.episode_id,
                    "guest": {
                        "id": a.guest.id,
                        "name": a.guest.name,
                        "occupation": a.guest.occupation,
                    },
                }
                for a in episode.appearances
            ],
        }

        return ep_dict, 200

    def delete(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return {"error": "Episode not found"}, 404

        db.session.delete(episode)
        db.session.commit()
        # 204 No Content => empty response body
        return "", 204


# 4. GET /guests
class Guests(Resource):
    def get(self):
        guests = Guest.query.all()
        data = [
            {
                "id": g.id,
                "name": g.name,
                "occupation": g.occupation,
            }
            for g in guests
        ]
        return data, 200


# 5. POST /appearances
class Appearances(Resource):
    def post(self):
        json_data = request.get_json() or {}

        rating = json_data.get("rating")
        episode_id = json_data.get("episode_id")
        guest_id = json_data.get("guest_id")

        # basic presence check – if anything is missing, treat as validation error
        if rating is None or episode_id is None or guest_id is None:
            return {"errors": ["validation errors"]}, 400

        try:
            appearance = Appearance(
                rating=rating,
                episode_id=episode_id,
                guest_id=guest_id,
            )
            db.session.add(appearance)
            db.session.commit()
        except Exception:
            db.session.rollback()
            # Match the spec: generic validation error message
            return {"errors": ["validation errors"]}, 400

        # Build response manually to match expected JSON
        resp = {
            "id": appearance.id,
            "rating": appearance.rating,
            "guest_id": appearance.guest_id,
            "episode_id": appearance.episode_id,
            "episode": {
                "id": appearance.episode.id,
                "date": appearance.episode.date,
                "number": appearance.episode.number,
            },
            "guest": {
                "id": appearance.guest.id,
                "name": appearance.guest.name,
                "occupation": appearance.guest.occupation,
            },
        }

        return resp, 201


# Register resources
api.add_resource(Index, "/")
api.add_resource(Episodes, "/episodes")
api.add_resource(EpisodeByID, "/episodes/<int:id>")
api.add_resource(Guests, "/guests")
api.add_resource(Appearances, "/appearances")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
