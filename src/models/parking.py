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

class ParkingReservation:
    def __init__(self, parking_id, day, hour):
        self.parking_id = parking_id
        self.day = day
        self.hour = hour

        self.status = 'available'
        self.user_id = None

    @staticmethod
    def update_reservation_status(parking_id, user_id, status):
        pass
    