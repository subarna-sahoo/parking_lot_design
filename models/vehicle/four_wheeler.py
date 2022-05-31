
from models.constants import VehicleType
from models.vehicle.vehicle import Vehicle


class FOUR_W(Vehicle):
    def __init__(self, vehicle_id:str, licence_no:str, contact_no:int, vehicle_type: VehicleType.FOUR_W):
        super().__init__(vehicle_id, licence_no, contact_no, vehicle_type)

    def get_parking_space(self):
        VehicleType.FOUR_W.value
    
    