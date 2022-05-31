
from models.constants import VehicleType
from models.vehicle.vehicle import Vehicle


class TWO_W(Vehicle):
    def __init__(self, license_number, ticket=None):
        super().__init__(license_number, VehicleType.TWO_W, ticket)
