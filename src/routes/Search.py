from flask import Blueprint, request, jsonify
from ..__init__ import gmaps

search = Blueprint('searchs', __name__)

@search.route('/search_autocomplete/<search_string>', methods=['GET'])
def search_autocomplete(search_string):
    args = request.args
    long, lat = args['long'], args['lat']

    autocomplete = gmaps.places_autocomplete(search_string, origin=f"{long}, {lat}", location=f"{long}, {lat}", radius=20000, language="pt-BR", components={"country": ['BR']}, strict_bounds=True)
    
    if autocomplete:
        return jsonify(autocomplete)
    
    return jsonify({"error": "No results found"})


@search.route('/search_parkings/<place_id>', methods=['GET'])
def search_parkings(place_id):
    # O FRONT -> origin, location e o search
    geocode = gmaps.geocode(language="pt-BR", region="BR", place_id=place_id)
    #places = gmaps.places('estacionamentos', location=geocode[0]["geometry"]["location"], language="pt-BR", radius=500, min_price=None, max_price=None, type="parking", page_token=None)
    places = gmaps.places_nearby(location=geocode[0]["geometry"]["location"], radius=None, language="pt-BR", rank_by="distance", type="parking")
    #testar places_nearby
    #falta distancia
    if places:
        places["geocode"] = geocode[0]["geometry"]["location"]
        return jsonify(places)
    return jsonify({"error": "No results found"})