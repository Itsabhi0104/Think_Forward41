# auth.py
from flask import Blueprint, request, jsonify
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify(msg="Email already exists"), 400

    user = User(
        first_name     = data['first_name'],
        last_name      = data['last_name'],
        email          = data['email'],
        password       = generate_password_hash(data['password']),
        age            = data.get('age'),
        gender         = data.get('gender'),
        state          = data.get('state'),
        street_address = data.get('street_address'),
        postal_code    = data.get('postal_code'),
        city           = data.get('city'),
        country        = data.get('country'),
        latitude       = data.get('latitude'),
        longitude      = data.get('longitude'),
        traffic_source = data.get('traffic_source')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(msg="User created"), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify(msg="Bad credentials"), 401

    token = create_access_token(identity=user.id)
    return jsonify(access_token=token), 200
