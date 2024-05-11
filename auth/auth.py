from flask import request, jsonify
from flask_bcrypt import Bcrypt
from models.user import User
from app import app, db
from utils.utils import hash_password, verify_password

class Auth:
    def login(data):
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and verify_password(data['password'], user.password):
            # login_user(user)
            return jsonify({'message': 'Logged in successfully'}), 200
        
        return jsonify({'message': 'Invalid credentials'}), 400

    def register(data):
        
        hashed_password = hash_password(data['password'])
        
        new_user = User(firstname=data['firstname'], lastname=data['lastname'], email=data['email'], password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'User created successfully'}), 201