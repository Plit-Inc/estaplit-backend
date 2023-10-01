from ..connection import client

class User:
    db = client['parking']
    collection = db['users']

    def __init__(self, phone, name, car):
        self.name = name
        self.phone = phone
        self.car = car

    @classmethod
    def initialize_db_and_collection(cls, db_name='parking', collection_name='users'):
        cls.db = client[db_name]
        cls.collection = cls.db[collection_name]

    @staticmethod
    def get_user_by_phone(phone):
        user = User.collection.find_one({'phone': phone})
        if user: return user
        return None
    
    @staticmethod
    def get_all_users():
        users = User.collection.find()
        return users
    
    @staticmethod
    def post_user(user):
        User.collection.insert_one(user)
        data = User.collection.find_one({'phone': user['phone']})
        return data
    
    @staticmethod
    def update_user(user):
        User.collection.update_one({'phone': user['phone']}, {'$set': user})

