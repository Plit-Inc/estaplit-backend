import pymongo
from ..connection import client
from datetime import datetime, timedelta

class Parking:
    def __init__(self, free_vacancies, total_vacancies, free_reservation, total_reservation, pricing, cancellation_policy, place_id):
        self.free_vacancies = free_vacancies
        self.total_vacancies = total_vacancies
        self.free_reservation = free_reservation
        self.total_reservation = total_reservation
        self.pricing = pricing
        self.cancellation_policy = cancellation_policy
        self.place_id = place_id
        self.reservations = []
    
    @staticmethod
    def get_parking_by_id(id):
        db = client['parking']
        collection = db['parking']
        parking = collection.find_one({'place_id': id})
        if parking:
            return parking
        return None
    
    @staticmethod
    def get_all_parking():
        db = client['parking']
        collection = db['parking']
        parking = collection.find()
        return parking
    
    @staticmethod
    def post_parking(parking):
        parking['reservations'] = []
        db = client['parking']
        collection = db['parking']
        collection.insert_one(parking)

    @staticmethod
    def delete_parking(parking):
        db = client['parking']
        collection = db['parking']
        collection.delete_one(parking)

    @staticmethod
    def generate_reservations(parking):
        db = client['parking']
        collection = db['parking']
        reservations = []
        today = datetime.now()
        if today.hour >= 9:
            today = today + timedelta(days=1)
        for i in range(7):
            day, month = today.day, today.month
            day_of_week = today.weekday()
            reservations.append([{'day': day, 'month': month, 'day_of_week': day_of_week, 'reservations': []}])
            for hour in range(10, 14):
                reservation = ParkingReservation(day, hour)
                reservations[i][0]['reservations'].append(reservation.__dict__)
            
            today = today + timedelta(days=1)

        collection.update_one({'place_id': parking['place_id']}, {'$set': {'reservations': reservations}})

    @staticmethod
    def make_reservation(parking, day, month, hour):
        db = client['parking']
        collection = db['parking']
        reservations = parking['reservations']
        for i in range(len(reservations)):
            reservation = reservations[i][0]
            if reservation['day'] == day and reservation['month'] == month:
                reservation['reservations'][hour-10]['status'] = 'unavailable'
                return True
        return None

class ParkingReservation:
    def __init__(self, day, hour):
        self.day = day
        self.hour = hour
        self.status = 'available'    