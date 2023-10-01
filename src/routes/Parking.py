from flask import Blueprint, request, jsonify
from ..models.parking import Parking
from ..__init__ import gmaps
from ..helpers.functions import get_distance

parking = Blueprint('parking', __name__)

@parking.route('/parking_route_test', methods=['GET'])
def parking_route_test():
    return {"user": "user", "password": "password"}

@parking.route('/get_parking/<place_id>', methods=['GET'])
def get_parking(place_id):
    args = request.args
    long, lat = args['long'], args['lat']
    geo_dict = {
        "geocode": {
            "lat": float(lat),
            "long": float(long)
        }
    }

    response = gmaps.place(place_id, language="pt-BR")

    parking_search = Parking.get_parking_by_id(place_id)
    #if data["generate_reservations"] == True: Parking.generate_reservations(parking_search)

    lat1, lng1 = response["result"]['geometry']['location']['lat'], response["result"]['geometry']['location']['lng']
    lat2, lng2 = geo_dict['geocode']['lat'], geo_dict['geocode']['long']

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

    parking = Parking.post_parking(data)

    Parking.generate_reservations(parking)

    return {"message": "Parking created successfully"}

@parking.route('delete_parking/<place_id>', methods=['DELETE'])
def delete_parking(place_id):

    Parking.delete_parking({place_id: place_id})

    return {"message": "Parking deleted successfully"}


@parking.route('/make_reservation', methods=['POST'])
def make_reservation():
    data = request.get_json()

    parking = Parking.get_parking_by_id(data['place_id'])

    if Parking.make_reservation(parking, data['day'], data['month'], data['hour']):
        return {"message": "Reservation made successfully"}
    
    return {"message": "Reservation failed"}