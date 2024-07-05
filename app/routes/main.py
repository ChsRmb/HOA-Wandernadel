import io

from flask import Blueprint, render_template, jsonify, send_file
from app.models import Location, GeneralSettings
import gpxpy
import gpxpy.gpx

main = Blueprint("main", __name__)


@main.route("/")
def map():
    general_settings = GeneralSettings.query.first()
    return render_template("map.html", settings=general_settings)


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
                "type": loc.loc_type.name,
                "enabled": loc.enabled
            }
            for loc in locations
        ]
    )


@main.route("/gpx/<int:location_id>")
def download_gpx(location_id):
    location = Location.query.get_or_404(location_id)
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(
        latitude=location.latitude,
        longitude=location.longitude,
        name=location.name
    ))
    gpx_data = gpx.to_xml()
    return send_file(
        io.BytesIO(gpx_data.encode("utf-8")),
        as_attachment=True,
        download_name=f"{location.name}.gpx",
        mimetype="application/gpx+xml",
    )
