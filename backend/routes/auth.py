from flask import Blueprint, request, jsonify
from models.user import User
from database import db

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(username=data["username"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered", "user_id": user.id})
