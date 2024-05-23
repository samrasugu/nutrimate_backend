from flask import jsonify
from models.disease import Disease
from app import db


class Diseases:
    def __init__(self):
        self.diseases = []

    def add_disease(data):
        new_disease = Disease(
            disease_name=data["disease_name"], description=data["description"]
        )

        db.session.add(new_disease)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Disease added successfully",
                    "disease": {
                        "disease_id": str(new_disease.disease_id),
                        "disease_name": new_disease.disease_name,
                        "description": new_disease.description,
                    },
                }
            ),
            200,
        )

    def get_disease(data):

        disease = Disease.query.filter_by(disease_name=data["disease"]).first()

        if disease:
            return (
                jsonify(
                    {
                        "message": "Disease found",
                        "disease": {
                            "disease_id": str(disease.disease_id),
                            "disease_name": disease.disease_name,
                            "description": disease.description,
                        },
                    }
                ),
                200,
            )

        return jsonify({"message": "Disease not found"}), 400
