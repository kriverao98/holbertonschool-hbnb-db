"""
Users controller module
"""

from flask import abort, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src.models.user import User

@jwt_required()
def get_users():
    """Returns all users"""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    users: list[User] = User.get_all()

    return [user.to_dict() for user in users]

@jwt_required()
def create_user():
    """Creates a new user"""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    data = request.get_json()

    try:
        user = User.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(400, "User already exists")

    return user.to_dict(), 201

@jwt_required()
def get_user_by_id(user_id: str):
    """Returns a user by ID"""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    user: User | None = User.get(user_id)

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200

@jwt_required()
def update_user(user_id: str):
    """Updates a user by ID"""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    data = request.get_json()

    try:
        user = User.update(user_id, data)
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200

@jwt_required()
def delete_user(user_id: str):
    """Deletes a user by ID"""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    if not User.delete(user_id):
        abort(404, f"User with ID {user_id} not found")

    return "", 204
