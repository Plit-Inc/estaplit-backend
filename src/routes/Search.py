from flask import Blueprint, request, jsonify
from ..__init__ import get_gmaps

search = Blueprint('searchs', __name__)

def get_parking_photo_url(place_details, max_width=400):
    if "photos" in place_details.get("result", {}):
        photo_reference = place_details["result"]["photos"][0].get("photo_reference")
        if photo_reference:
            gmaps = get_gmaps()
            # Use a chave de API obtida no __init__.py
            api_key = gmaps.api_key
            return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photoreference={photo_reference}&key={api_key}"
    return None

@search.route('/search_autocomplete', methods=['POST'])
def search_autocomplete():
    data = request.get_json()
    # O FRONT -> origin, location e o search
    gmaps = get_gmaps()
    autocomplete = gmaps.places_autocomplete(data['search'], origin="-8.112651, -34.965816", location="-8.112651, -34.965816", radius=20000, language="pt-BR", components={"country": ['BR']}, strict_bounds=True)
    
    if autocomplete:
        return jsonify(autocomplete)
    
    return jsonify({"error": "No results found"})


@search.route('/search_parkings', methods=['POST'])
def search_parkings():
    data = request.get_json()
    # O FRONT -> origin, location e o search
    gmaps = get_gmaps()
    geocode = gmaps.geocode(language="pt-BR", region="BR", place_id=data['place_id'])
    #places = gmaps.places('estacionamentos', location=geocode[0]["geometry"]["location"], language="pt-BR", radius=500, min_price=None, max_price=None, type="parking", page_token=None)
    places = gmaps.places_nearby(location=geocode[0]["geometry"]["location"], radius=None, language="pt-BR", rank_by="distance", type="parking")
    #testar places_nearby

    #falta distancia

    if places:
        places["geocode"] = geocode[0]["geometry"]["location"]

        # Agora, para cada lugar, obtenha os detalhes do lugar para obter a referência da foto
        for place in places.get("results", []):
            place_id = place.get("place_id")
            place_details = gmaps.place(place_id, language="pt-BR", region="BR")
            if place_details and "result" in place_details:
                result = place_details["result"]
                # Obtenha a URL da imagem do estacionamento
                photo_url = get_parking_photo_url(place_details)
                if photo_url:
                    place["photo_url"] = photo_url

        return jsonify(places)
    
    return jsonify({"error": "No results found"})
