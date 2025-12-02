from flask import Blueprint, request, jsonify
from . import db, bcrypt
from .models import User  
import logging


from flask_login import login_user, logout_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
logger = logging.getLogger(__name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    user_exists = User.query.filter_by(username=username).first()
    if user_exists:
        return jsonify({"error": "Username already exists."}), 400

    # Hashes the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"New user created: {username}")
        return jsonify({"message": "Account created successfully! Please log in."}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating user: {e}")
        return jsonify({"error": "Database error, could not create user."}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    user = User.query.filter_by(username=username).first()

    # Check if user exists and password is correct
    if not user or not bcrypt.check_password_hash(user.password, password):
        logger.warning(f"Failed login attempt for user: {username}")
        return jsonify({"error": "Invalid username or password."}), 401

   
    login_user(user, remember=True)
    
    logger.info(f"User logged in successfully: {username}")
    return jsonify({"message": "Login successful!"}), 200

@auth_bp.route('/logout')
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully."})
