from services.parking_service import ParkingService
from models.payment.basic_payment import BasicPayment
import connexion
from flask import jsonify, request

app = connexion.App(__name__, specification_dir="./")
# app.add_api("swagger.yml")


# CUT ---------------------------------
# from response import SchemaValidationError, +MovieAlreadyExistsError, \
# +InternalServerError, UpdatingMovieError, DeletingMovieError, +MovieNotExistsError
# +

service = ParkingService(10, payment=BasicPayment())


@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "message": "server health is good"
    })


@app.route('/vehicle/history', methods=['POST'])
def get_vehicle_history():
    # GET /vehicle/history
    data = request.get_json()
    try:
        resp = service.get_vehicle_history(data["licence_no"])
        return {
            "message": "successful",
            "tickets": resp
        }, 200

    except Exception as message:
        print(message)
        return {
            "message": "error"}, 400


@app.route('/vehicle', methods=['POST'])
def park_vehicle():
    # POST /vehicle/park
    data = request.get_json()
    try:
        resp = service.get_ticket(data["licence_no"], data["contact_no"], data["vehicle_type"])
        if (resp==None)
        return {
            "message": "successful",
            "ticket_id": resp.ticket_id
        }, 200

    except Exception as message:
        print(message)
        return {
            "message": "error"
        }, 400


# @app.route('/vehicle', methods=['GET', 'POST'])
# def park_vehicle():
#     # POST /vehicle/park
#     data = request.get_json()
#     try:
#         resp = service.get_ticket(data["licence_no"], data["contact_no"], data["vehicle_type"])
#         return {
#             "message": "successful",
#             "ticket_id": resp.ticket_id
#         }, 200

#     except Exception as message:
#         print(message)
#         return {
#             "message": "error"
#         }, 400

# CUT ---------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
