from flask import request, jsonify
from flask_bcrypt import Bcrypt
from models.user import User
from app import db
from models.user_profile import UserProfile
from utils.utils import hash_password, verify_password


class Auth:
    def login(data):

        user = User.query.filter_by(email=data["email"]).first()

        if user and verify_password(data["password"], user.password):
            # fetch user profile
            profile = UserProfile.query.filter_by(user_id=user.id).first()
            if not profile:
                return jsonify({"error": "Profile not found"}), 404

            return (
                jsonify(
                    {
                        "message": "Logged in successfully",
                        "user": {
                            "id": str(user.id),
                            "firstname": user.firstname,
                            "lastname": user.lastname,
                            "email": user.email,
                        },
                        "profile": profile_to_dict(profile),
                    }
                ),
                200,
            )

        return jsonify({"message": "Invalid credentials"}), 400

    def register(data):

        hashed_password = hash_password(data["password"])

        new_user = User(
            firstname=data["firstname"],
            lastname=data["lastname"],
            email=data["email"],
            password=hashed_password,
        )

        db.session.add(new_user)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "User created successfully",
                    "user": {
                        "id": str(new_user.id),
                        "firstname": new_user.firstname,
                        "lastname": new_user.lastname,
                        "email": new_user.email,
                    },
                }
            ),
            201,
        )

    def create_profile(data):
        user_id = data.get("user_id")
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Check if the user already has a profile
        existing_profile = UserProfile.query.filter_by(user_id=user_id).first()
        if existing_profile:
            return jsonify({"error": "User profile already exists"}), 400

        new_profile = UserProfile(
            age=data.get("age"),
            gender=data.get("gender"),
            illnesses=data.get("illnesses"),
            weight=data.get("weight"),
            height=data.get("height"),
            location=data.get("location"),
            food_preferences=data.get("food_preferences"),
            user_id=user_id,
        )

        db.session.add(new_profile)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "User profile created successfully",
                    "profile": profile_to_dict(new_profile),
                }
            ),
            201,
        )

    def get_user_profile(data):
        profile = UserProfile.query.filter_by(user_id=data["user_id"]).first()
        if not profile:
            return jsonify({"error": "Profile not found"}), 404

        return jsonify({"profile": profile_to_dict(profile)})


def profile_to_dict(profile):
    return {
        "id": str(profile.id),
        "age": str(profile.age),
        "gender": profile.gender,
        "illnesses": profile.illnesses,
        "weight": str(profile.weight),
        "height": str(profile.height),
        "location": profile.location,
        "food_preferences": profile.food_preferences,
        "user_id": str(profile.user_id),
    }
