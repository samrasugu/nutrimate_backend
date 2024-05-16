from flask import Flask, request, jsonify
from chat import BotClient
from recommend import Recommend
import os
from flask_sqlalchemy import SQLAlchemy
from auth import auth
from database_config import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRESDB_URL')

# secret key for session management using flask
app.secret_key = os.getenv('SECRET_KEY')

db.init_app(app)

# debug mode
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def api():
    return "Hello, World!"

@app.route('/chat', methods=['POST'])
def recognize_text():
    
    message = request.get_json()['message']
    
    response = BotClient().recognize_text(message=message)
    
    return jsonify(response)

@app.route('/recommend', methods=['POST'])
def recommend():
    
    message = request.get_json()['message']
    
    response = Recommend().recommend(message=message)
    
    return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    return auth.Auth.login(data)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    return auth.Auth.register(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)