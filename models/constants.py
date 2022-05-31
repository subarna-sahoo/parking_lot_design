from enum import Enum

class VehicleType(Enum):
    """ This assign the parking price required as respect to VehicleType """
    FOUR_W, TWO_W ="four","two"



class TicketStatus(Enum):
    RESERVED, PAID = "reserved", "paid"
