from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

app = Flask(__name__)

def create_app():
    db.init_app(app)
    ma.init_app(app)

    @app.route('/')
    def hello():
        return 'adfadfs'

    return app