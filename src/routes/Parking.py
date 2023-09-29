from flask import Blueprint, request
from ..models import parking

parking = Blueprint('parking', __name__)

@parking.route('/parking_route_test', methods=['GET'])
def parking_route_test():
    return {"user": "user", "password": "password"}

@parking.route('/parking', methods=['GET'])
def get_parking():
    return parking.get_parking()

@parking.route('/parking', methods=['POST'])
def post_parking():
    return parking.post_parking(request.get_json())