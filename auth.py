from flask import Blueprint, request, jsonify
from app import db, bcrypt
from sqlalchemy import func
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    saved_chats = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "saved_chats": self.saved_chats or [],
            "created_at": self.created_at.isoformat()
        }

def get_user_by_username(username: str):
    return User.query.filter(func.lower(User.username) == username.lower()).first()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(force=True)
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"ok": False, "error": "username and password required"}), 400

    if get_user_by_username(username):
        return jsonify({"ok": False, "error": "username already taken"}), 409

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, password=pw_hash, saved_chats=[])
    db.session.add(user)
    db.session.commit()

    return jsonify({"ok": True, "user": user.to_dict()}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = get_user_by_username(username)
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"ok": False, "error": "invalid username or password"}), 401

    return jsonify({"ok": True, "user": user.to_dict()}), 200

@auth_bp.route("/_all_users", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify({"ok": True, "users": [u.to_dict() for u in users]}), 200
