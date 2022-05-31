from models.vehicle.vehicle import Vehicle


class ParkingSlot:
    def __init__(self, slot_id:int, is_reserved:bool=False, vehicle_id: str=None):
        self._slot_id = slot_id
        self._is_reserved = is_reserved
        self._vehicle_id = vehicle_id
    
    def is_available(self):
        return self._vehicle_id == None

    def park(self, _vehicle_id: Vehicle):
        self._vehicle_id = _vehicle_id

    def remove_vehicle(self):
        self._vehicle = None