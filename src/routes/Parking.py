from flask import Blueprint, request, jsonify
from ..models.parking import Parking
from ..__init__ import gmaps
from ..helpers.functions import get_distance

parking = Blueprint('parking', __name__)

@parking.route('/parking_route_test', methods=['GET'])
def parking_route_test():
    return {"user": "user", "password": "password"}

@parking.route('/get_parking', methods=['POST'])
def get_parking():
    data = request.get_json()

    response = gmaps.place(data['place_id'], language="pt-BR")

    parking_search = Parking.get_parking_by_id(data['place_id'])
    #if data["generate_reservations"] == True: Parking.generate_reservations(parking_search)

    lat1, lng1 = response["result"]['geometry']['location']['lat'], response["result"]['geometry']['location']['lng']
    lat2, lng2 = data['geocode']['lat'], data['geocode']['lng']

    print(get_distance(lat1, lng1, lat2, lng2))
    directions = gmaps.directions((lat1, lng1), (lat2, lng2), mode="walking", language="pt-BR")


    if parking_search:
        response["bd_data"] = parking_search
        response["bd_data"].pop("_id")
        return jsonify(response)

    return response

@parking.route('/create_parking', methods=['POST'])
def create_parking():
    data = request.get_json()

    Parking.post_parking(data)

    return {"message": "Parking created successfully"}

@parking.route('delete_parking', methods=['POST'])
def delete_parking():
    data = request.get_json()

    Parking.delete_parking(data)

    return {"message": "Parking deleted successfully"}


@parking.route('/make_reservation', methods=['POST'])
def make_reservation():
    data = request.get_json()

    parking = Parking.get_parking_by_id(data['place_id'])

    if Parking.make_reservation(parking, 30, 9, 12):
        return {"message": "Reservation made successfully"}
    
    return {"message": "Reservation failed"}