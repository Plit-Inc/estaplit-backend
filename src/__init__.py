from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask import Markup
import googlemaps
from dotenv import load_dotenv
import os
from flask_restx import Api, Resource, fields




load_dotenv()
app = Flask(__name__)

google_api_key = os.getenv('KEY')

gmaps = googlemaps.Client(key=google_api_key)
api = Api(app, version='1.0', title='Estaplit-Backend')

ns = api.namespace('parking')

n_search = api.namespace('search')

reservation_input_model = api.model('Input', {
    'place_id': fields.String(required=True, description='ID do local'),
    'day': fields.Integer(required=True, description='Dia'),
    'month': fields.Integer(required=True, description='Mês'),
    'hour': fields.Integer(required=True, description='Hora')
})

get_place_id_input_model = api.model('Delete', {
    'place_id': fields.String(required=True, description='ID do local')
})

reservation_create_parking_input_model = api.model('InputData', {
    'place_id': fields.String(required=True, description='ID do local'),
    'geocode': fields.Nested(api.model('Geocode', {
        'lat': fields.Float(required=True, description='Latitude'),
        'lng': fields.Float(required=True, description='Longitude')
    }), description='Coordenadas geográficas'),
    'generate_reservations': fields.Boolean(required=False, description='Gerar reservas')
})

search_input_model = api.model('SearchInput', {
    'search': fields.String(required=True, description='Termo de pesquisa'),
    'location': fields.String(required=True, description='Localização no formato "latitude, longitude"')
})


def get_gmaps():
    return gmaps

def create_app():
    from .routes.Search import search
    from .routes.Parking import parking

    app.register_blueprint(parking, url_prefix="/parking")
    app.register_blueprint(search, url_prefix="/search")

    @api.route('/hello')
    class HelloWorld(Resource):
        def get(self):
            return 'hello'



    @ns.route('/make_reservation')
    class PostResource(Resource):
        @ns.expect(reservation_input_model)  
        def post(self):
            data = request.json  
            place_id = data['place_id']
            day = data['day']
            month = data['month']
            hour = data['hour']

            response = {
                'message': 'Dados recebidos com sucesso',
            }
            return response, 200
        
    @ns.route('-/delete_parking')
    class PostResource(Resource):
        @ns.expect(get_place_id_input_model)  
        def post(self):
            data = request.json  
            place_id = data['place_id']

            response = {
                'message': 'Parking deleted successfully',
            }
            return response, 200

    @ns.route('/create_parking')
    class PostResource(Resource):
        @ns.expect(reservation_create_parking_input_model)  
        def post(self):
            data = request.json  
            return {"bd_data": "{}", "data": data}, 201

    @ns.route('/get_parking')
    class PostResource(Resource):
        @ns.expect(reservation_create_parking_input_model)  
        def post(self):
            data = request.json  
            return {"message": "Dados recebidos com sucesso", "data": data}, 201

    @n_search.route('/search_parkings')
    class PostResource(Resource):
        @n_search.expect(get_place_id_input_model)  
        def post(self):
            data = request.json  
            return {"message": "Dados recebidos com sucesso", "data": data}, 201

    @n_search.route('/search_autocomplete')
    class PostResource(Resource):
        @n_search.expect(search_input_model)  
        def post(self):
            data = request.json  
            return {"message": "Dados recebidos com sucesso", "data": data}, 201
# -- 

    return app