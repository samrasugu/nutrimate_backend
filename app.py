from flask import Flask, request, jsonify
from chat import BotClient
from recommend import Recommend
import os
from flask_sqlalchemy import SQLAlchemy
from auth import auth
from database_config import db
from diseases import diseases
from locations import locations

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRESDB_URL")

# secret key for session management using flask
app.secret_key = os.getenv("SECRET_KEY")

db.init_app(app)

# debug mode
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def api():
    return "Hello, World!"


@app.route("/chat", methods=["POST"])
def recognize_text():

    message = request.get_json()["message"]

    response = BotClient().recognize_text(message=message)

    return jsonify(response)


@app.route("/recommend", methods=["POST"])
def recommend():

    message = request.get_json()["message"]

    response = Recommend().recommend(message=message)

    return jsonify(response)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    return auth.Auth.login(data)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    return auth.Auth.register(data)


@app.route("/create_profile", methods=["POST"])
def create_profile():
    data = request.get_json()

    return auth.Auth.create_profile(data)


@app.route("/add_disease", methods=["POST"])
def add_disease():
    data = request.get_json()

    return diseases.Diseases.add_disease(data)


@app.route("/get_disease", methods=["POST"])
def get_disease():
    data = request.get_json()

    return diseases.Diseases.get_disease(data)


@app.route("/add_location", methods=["POST"])
def add_location():
    data = request.get_json()

    return locations.Locations.add_location(data)


@app.route("/get_location", methods=["POST"])
def get_location():
    data = request.get_json()

    return locations.Locations.get_location(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
