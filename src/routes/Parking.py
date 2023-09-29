from flask import Blueprint, request
from ..models import parking
from ..__init__ import gmaps

parking = Blueprint('parking', __name__)

@parking.route('/parking_route_test', methods=['GET'])
def parking_route_test():
    return {"user": "user", "password": "password"}

@parking.route('/get_parking', methods=['POST'])
def get_parking():
    data = request.get_json()

    response = gmaps.place(data['place_id'], language="pt-BR")

    parking = parking.get_parking_by_id(data['place_id'])
    if parking:
        response["bd_data"] = parking
        return response

    return response