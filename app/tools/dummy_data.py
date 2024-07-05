from app.models import User, LocationType, GeneralSettings
from app import db


def create_dummy_data():
    if not User.query.first():
        example = User(username="admin", email="example@example.com", password="admin")
        db.session.add(example)
        db.session.commit()

    if not LocationType.query.first():
        type_example = [
            {
                "name": "Normal",
                "description": "Single hikingpin"
            },
            {
                "name": "Multi",
                "description": "This is a multi hikingpin, with multiple stations"
            },
            {
                "name": "Mystery",
                "description": "First you have to solve a puzzle to find the hikingpin"
            }
        ]

        for types in type_example:
            example = LocationType(name=types["name"], description=types["description"])
            db.session.add(example)
        db.session.commit()

    if not GeneralSettings.query.first():
        example = GeneralSettings(
            latitude=52.46217,
            longitude=10.60441,
            zoom_level=18,
        )
        db.session.add(example)
        db.session.commit()