from models.constants import VehicleType


class VehicleHourlyPrice:
    def __init__(self, vehicle_type: VehicleType, price: float):
        # self.id 
        self.vehicle_type = vehicle_type
        self.price = price
