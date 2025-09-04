from flask import Blueprint, request, jsonify
from models.user import create_user, get_user_by_email
import bcrypt
import jwt
import os
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)
JWT_SECRET = os.getenv("JWT_SECRET")

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    if get_user_by_email(email):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    create_user(first_name, last_name, email, hashed_password)
    return jsonify({"message": "User created successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = get_user_by_email(email)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
        token = jwt.encode({
            "user_id": user[0],
            "exp": datetime.utcnow() + timedelta(hours=24)
        }, JWT_SECRET, algorithm="HS256")
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid password"}), 401
