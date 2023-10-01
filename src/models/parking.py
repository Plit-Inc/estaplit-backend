import pymongo
from ..connection import client
from datetime import datetime, timedelta

class Parking:
    db = client['parking']
    collection = db['parking']

    def __init__(self, free_vacancies, total_vacancies, free_reservation, total_reservation, pricing, cancellation_policy, place_id):
        self.free_vacancies = free_vacancies
        self.total_vacancies = total_vacancies
        self.free_reservation = free_reservation
        self.total_reservation = total_reservation
        self.pricing = pricing
        self.cancellation_policy = cancellation_policy
        self.place_id = place_id
        self.reservations = []
        self.is_open = False
        self.phone = None

    @classmethod
    def initialize_db_and_collection(cls, db_name='parking', collection_name='parking'):
        cls.db = client[db_name]
        cls.collection = cls.db[collection_name]
    
    @staticmethod
    def get_parking_by_id(id):
        parking = Parking.collection.find_one({'place_id': id})
        if parking: return parking
        return None
    
    @staticmethod
    def get_parking_by_owner(phone):
        parking = Parking.collection.find_one({'owner_phone': phone})
        if parking: return parking
        return None

    @staticmethod
    def get_all_parking():
        parking = Parking.collection.find()
        return parking
    
    @staticmethod
    def post_parking(parking):
        parking['reservations'] = []
        Parking.collection.insert_one(parking)
        data = Parking.collection.find_one({'place_id': parking['place_id']})
        return data
    
    @staticmethod
    def update_parking(parking):
        Parking.collection.update_one({'place_id': parking['place_id']}, {'$set': parking})

    @staticmethod
    def delete_parking(parking):
        Parking.collection.delete_one(parking)

    @staticmethod
    def generate_reservations(parking):
        week_days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        today = datetime.now()

        # Adjust today's date if it's past 9 AM
        if today.hour >= 9:
            today += timedelta(days=1)

        reservations = []

        for _ in range(7):
            day, month = today.day, today.month
            day_of_week = week_days[today.weekday()]

            # Generate reservations for each hour from 10 to 13
            reservations_per_day = [{'hour': hour, 'isAvailable': True} for hour in range(10, 14)]

            reservations.append({
                'day': day,
                'month': month,
                'day_of_week': day_of_week,
                'reservations': reservations_per_day
            })

            today += timedelta(days=1)

        # Update the reservations in the parking document
        Parking.collection.update_one({'place_id': parking['place_id']}, {'$set': {'reservations': reservations}})

    @staticmethod
    def make_reservation(parking, day, month, hour):
        for reservation in parking['reservations']:
            if reservation['day'] == day and reservation['month'] == month:
                for timeslot in reservation['reservations']:
                    if timeslot['hour'] == hour:
                        if timeslot['isAvailable']:
                            timeslot['isAvailable'] = False
                            Parking.update_parking(parking)
                            return True  # Reservation successful
                        else:
                            return False  # Slot is already taken
        return None
    
    @staticmethod
    def update_parking_owner(phone, data):
        parking = Parking.get_parking_by_owner(phone)
        if parking:
            parking['phone'] = data['phone']
            Parking.update_parking(data)
            return parking
        return None