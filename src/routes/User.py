from flask import Blueprint, request, jsonify
from ..models.user import User
from ..__init__ import gmaps


user = Blueprint('user', __name__)

@user.route('/user_route_test', methods=['GET'])
def user_route_test():
    return {"user": "user", "password": "password"}

@user.route('/get_user/<phone>', methods=['GET'])
def get_user(phone):
    user = User.get_user_by_phone(phone)

    if user:
        user.pop("_id")
        return jsonify(user)

    return {"error": "User not found"}


@user.route('/get_all_users', methods=['GET'])
def get_all_users():
    users = User.get_all_users()

    if users:
        return jsonify(users)

    return {"error": "Users not found"}

@user.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()

    user = User.post_user(data)

    if user:
        user.pop("_id")
        return jsonify(user)

    return {"error": "User not created"}

