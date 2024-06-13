from flask import jsonify
from app import db
from models.location import Location
from sqlalchemy import or_


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

        search_term = f"%{data['name']}%"

        locations = Location.query.filter(Location.name.ilike(search_term)).all()

        if locations:
            location_list = [
                {
                    "id": str(location.id),
                    "name": location.name,
                    "description": location.description,
                }
                for location in locations
            ]

            return (
                jsonify(
                    {
                        "message": "Location found",
                        "locations": location_list,
                    }
                ),
                200,
            )

        return jsonify({"message": "Location not found"}), 400
