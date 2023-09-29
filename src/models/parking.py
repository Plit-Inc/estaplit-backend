import pymongo

class Parking:
    def __init__(self, name, address, free_vacancies, total_vacancies, free_reservation, total_reservation, pricing, opening_hours, cancellation_policy):
        self.name = name
        self.address = address
        self.free_vacancies = free_vacancies
        self.total_vacancies = total_vacancies
        self.free_reservation = free_reservation
        self.total_reservation = total_reservation
        self.pricing = pricing
        self.opening_hours = opening_hours
        self.cancellation_policy = cancellation_policy
    
    @staticmethod
    def get_parking_by_id(id):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['parking']
        collection = db['parking']
        parking = collection.find_one({'_id': id})
        return parking
    
    @staticmethod
    def get_all_parking():
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['parking']
        collection = db['parking']
        parking = collection.find()
        return parking
    
    @staticmethod
    def post_parking(parking):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['parking']
        collection = db['parking']
        collection.insert_one(parking)

class ParkingReservation:
    def __init__(self, parking_id, day, hour):
        self.parking_id = parking_id
        self.day = day
        self.hour = hour

        self.status = 'available'
        self.user_id = None

    
    