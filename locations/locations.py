from flask import jsonify
from app import db
from models.location import Location


class Locations:
    def __init__(self):
        self.diseases = []

    def add_location(data):
        new_location = Location(name=data["name"], description=data["description"])

        db.session.add(new_location)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Location added successfully",
                    "location": {
                        "id": str(new_location.id),
                        "name": new_location.name,
                        "description": new_location.description,
                    },
                }
            ),
            200,
        )

    def get_location(data):

        location = Location.query.filter_by(name=data["name"]).first()

        if location:
            return (
                jsonify(
                    {
                        "message": "Location found",
                        "location": {
                            "id": str(location.id),
                            "name": location.name,
                            "description": location.description,
                        },
                    }
                ),
                200,
            )

        return jsonify({"message": "Location not found"}), 400
