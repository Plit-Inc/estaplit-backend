from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask import Markup
from .routes.Search import search
from .routes.Parking import parking
import googlemaps
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)

google_api_key = os.getenv('KEY')

gmaps = googlemaps.Client(key=google_api_key)

def create_app():
    app.register_blueprint(parking, url_prefix="/parking")
    #app.register_blueprint(search, url_prefix="/search")

    @app.route('/')
    def hello():
        return {"user": "user", "password": "password"}

############ SEARCH ROUTE
    @app.route('/search_autocomplete', methods=['POST'])
    def search_autocomplete():
        data = request.get_json()
        # O FRONT -> origin, location e o search
        autocomplete = gmaps.places_autocomplete(data['search'], origin="-8.112651, -34.965816", location="-8.112651, -34.965816", radius=15000, language="pt-BR", components={"country": ['BR']}, strict_bounds=True, types="geocode")
        
        if autocomplete:
            return jsonify(autocomplete)
        
        return jsonify({"error": "No results found"})


    @app.route('/search_parkings', methods=['POST'])
    def search_parkings():
        data = request.get_json()
        # O FRONT -> origin, location e o search
        geocode = gmaps.geocode(language="pt-BR", region="BR", place_id=data['place_id'])
        print(geocode)
        autocomplete = gmaps.places('estacionamentos em ' + data['search'], location=geocode, language="pt-BR", radius=1000, min_price=None, max_price=None, open_now=False, type="parking", page_token=None)
        
        if autocomplete:
            return jsonify(autocomplete)
        
        return jsonify({"error": "No results found"})


    return app
