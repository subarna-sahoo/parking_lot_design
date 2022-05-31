from ..constants import VehicleType


class Vehicle:
    def __init__(self, vehicle_id:str, licence_no:str, contact_no:str, vehicle_type: VehicleType):
        self.vehicle_id = vehicle_id #auto
        self.licence_no = licence_no # (unique - key)
        self.contact_no = contact_no
        self.vehicle_type = vehicle_type

    def __str__(self):
        return f"{self.vehicle_type} [licence_no=" + {self.licence_no} + ", contact_no=" + {self.contact_no} + "]"
