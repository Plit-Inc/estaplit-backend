from flask import Blueprint, request, jsonify
from ..__init__ import gmaps

search = Blueprint('searchs', __name__)

@search.route('/search_autocomplete', methods=['POST'])
def search_autocomplete():
    data = request.get_json()
    # O FRONT -> origin, location e o search
    autocomplete = gmaps.places_autocomplete(data['search'], origin="-8.112651, -34.965816", location="-8.112651, -34.965816", radius=15000, language="pt-BR", components={"country": ['BR']}, strict_bounds=True, types="geocode")
    
    if autocomplete:
        return jsonify(autocomplete)
    
    return jsonify({"error": "No results found"})


@search.route('/search_parkings', methods=['POST'])
def search_parkings():
    data = request.get_json()
    # O FRONT -> origin, location e o search
    geocode = gmaps.geocode(language="pt-BR", region="BR", place_id=data['place_id'])
    autocomplete = gmaps.places('estacionamentos', location=geocode[0]["geometry"]["location"], language="pt-BR", radius=500, min_price=None, max_price=None, open_now=True, type="parking", page_token=None)
    
    #testar places_nearby

    if autocomplete:
        return jsonify(autocomplete)
    
    return jsonify({"error": "No results found"})