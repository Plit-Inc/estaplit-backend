from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask import Markup
import googlemaps
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)

google_api_key = os.getenv('KEY')

gmaps = googlemaps.Client(key=google_api_key)

def get_gmaps():
    return gmaps

def create_app():
    from .routes.Search import search
    from .routes.Parking import parking

    app.register_blueprint(parking, url_prefix="/parking")
    app.register_blueprint(search)

    @app.route('/')
    def hello():
        return {"user": "user", "password": "password"}

    return app