from flask import Flask
from pymongo import MongoClient
from flask import Markup
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
MONGO_URI = os.environ.get('MONGO_URI')

cluster = MongoClient('MONGO_URI')
db      = cluster['estaplit-bd']
col     = db['parking']

def create_app():
    @app.route('/')
    def hello():
        return {"user": "user", "password": "password"}

    @app.route('/user', methods=['GET', 'POST'])
    def user():
        return {"user": "user", "password": "password"}

    return app

    @app.route('/parking', methods=['POST'])
    def create_parking():
        print("teste")
        name = request.json['name']
        address = request.json['address']
        free_vacancies = request.json['free_vacancies']
        total_vacancies = request.json['total_vacancies']
        free_reservation = request.json['free_reservation']
        total_reservation = request.json['total_reservation']
        pricing = request.json['pricing']
        opening_hours = request.json['opening_hours']
        cancellation_policy = request.json['cancellation_policy']

        parking_dict = {
            "name": name,
            "address": address,
            "free_vacancies": free_vacancies,
            "total_vacancies": total_vacancies,
            "free_reservation": free_reservation,
            "total_reservation": total_reservation,
            "pricing": pricing,
            "opening_hours": opening_hours,
            "cancellation_policy": cancellation_policy
        }

        col.insert_one(parking_dict)
        return "success"