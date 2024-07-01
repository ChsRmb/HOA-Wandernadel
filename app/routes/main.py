from flask import Blueprint, render_template
from app.models import Location
from flask import jsonify

main = Blueprint("main", __name__)


@main.route("/")
def map():
    locations = Location.query.all()
    return render_template("map.html", locations=locations)


@main.route("/api/locations")
def get_locations():
    locations = Location.query.all()
    return jsonify(
        [
            {
                "id": loc.id,
                "name": loc.name,
                "latitude": loc.latitude,
                "longitude": loc.longitude,
                "difficulty": loc.difficulty_level,
                "terrain": loc.terrain_level,
                "image_url": loc.image_url,
                "description": loc.description,
            }
            for loc in locations
        ]
    )
