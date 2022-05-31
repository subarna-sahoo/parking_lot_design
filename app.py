from exception.api_response import ParkingServiceException
from services.parking_service import ParkingService
from models.payment.basic_payment import BasicPayment
import connexion
from flask import jsonify, request
import json

app = connexion.App(__name__, specification_dir="./")

service = ParkingService(10, payment=BasicPayment())


@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "message": "server health is good"
    })


@app.route('/vehicle/history', methods=['POST'])
def get_vehicle_history():
    # GET /vehicle/history
    # GET /vehicle/history?licence_no=xyz
    licence_no = request.args.get("licence_no", None)
    try:
        if licence_no:
            resp = service.get_vehicle_history(licence_no)
        else:
            resp = service.get_all_vehicle_history()

        return {
            "message": "successful",
            "tickets": [vehicle.__dict__ for vehicle in resp]
        }, 200
    except ParkingServiceException as e:
        return {
            "message": e.args[0]
        }, 400
    except Exception as e:
        return {
            "message": "general exception occured"
        }, 500


@app.route('/vehicle/park', methods=['POST'])
def park_vehicle():
    # POST /vehicle/park
    data = request.get_json()
    try:
        resp = service.get_ticket(data["licence_no"], data["contact_no"], data["vehicle_type"])
        return {
            "message": "successful",
            "ticket": resp.__dict__
        }, 200
    except ParkingServiceException as e:
        return {
            "message": e.args[0]
        }, 400
    except Exception as e:
        return {
            "message": "general exception occured"
        }, 500


@app.route('/vehicle/checkout/<ticket_id>', methods=['PUT'])
def checkout_vehicle(ticket_id):
    # PUT /vehicle/checkout/:ticket_id
    try:
        resp = service.checkout_vehicle(ticket_id)
        return {
            "message": "successful",
            "response": resp.__dict__
        }, 200

    except ParkingServiceException as e:
        return {
            "message": e.args[0]
        }, 400
    except Exception as e:
        return {
            "message": "general exception occured"
        }, 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
