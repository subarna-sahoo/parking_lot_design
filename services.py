from flask import jsonify, request
from models.payment.basic_payment import BasicPayment
from services.parking_service import ParkingService

service = ParkingService(10, payment = BasicPayment())


def root():
    print(request)
    return jsonify({
        "req": "server health is good"
    })

def get_vehicle_history(licence_no):
    # GET /vehicle/history
    return service.get_vehicle_history(licence_no)
