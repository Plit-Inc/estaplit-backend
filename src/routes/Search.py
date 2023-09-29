from flask import Blueprint, request

search = Blueprint('search', __name__)

@search.route('/', methods=['POST'])
def search():
    data = request.get_json()
    print(data)
    
