"""
This module contains the routes for the users endpoints.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User
import bcrypt

from src import app

from src.controllers.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)

users_bp = Blueprint("users", __name__, url_prefix="/users")

users_bp.route("/", methods=["GET"])(get_users)
users_bp.route("/", methods=["POST"])(create_user)

users_bp.route("/<user_id>", methods=["GET"])(get_user_by_id)
users_bp.route("/<user_id>", methods=["PUT"])(update_user)
users_bp.route("/<user_id>", methods=["DELETE"])(delete_user)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return 'Wrong username or password', 401