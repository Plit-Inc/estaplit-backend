from flask import Blueprint, request, jsonify
from ..__init__ import gmaps

search = Blueprint('searchs', __name__)

@search.route('/search_autocomplete', methods=['POST'])
def search_autocomplete():
    data = request.get_json()
    # O FRONT -> origin, location e o search
    autocomplete = gmaps.places_autocomplete(data['search'], origin="-8.112651, -34.965816", location="-8.112651, -34.965816", radius=20000, language="pt-BR", components={"country": ['BR']}, strict_bounds=True)
    
    if autocomplete:
        return jsonify(autocomplete)
    
    return jsonify({"error": "No results found"})


@search.route('/search_parkings', methods=['POST'])
def search_parkings():
    data = request.get_json()
    # O FRONT -> origin, location e o search
    geocode = gmaps.geocode(language="pt-BR", region="BR", place_id=data['place_id'])
    #places = gmaps.places('estacionamentos', location=geocode[0]["geometry"]["location"], language="pt-BR", radius=500, min_price=None, max_price=None, type="parking", page_token=None)
    places = gmaps.places_nearby(location=geocode[0]["geometry"]["location"], radius=None, language="pt-BR", rank_by="distance", type="parking")
    #testar places_nearby

    #falta distancia

    if places:
        places["geocode"] = geocode[0]["geometry"]["location"]
        return jsonify(places)
    
    return jsonify({"error": "No results found"})