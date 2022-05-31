from datetime import datetime
from models.constants import TicketStatus

class ReservationTicket:
    def __init__(self, ticket_id:str, licence_no:str, parking_slot_id:str, hourly_price: float):
        self.ticket_id = ticket_id #auto
        self.licence_no = licence_no
        self.parking_slot_id = parking_slot_id
        self.ticket_status = TicketStatus.RESERVED.value
        self.hourly_price = hourly_price
        self.start_time = datetime.now()
        self.end_time = None

        self.total_price = None


    def __str__(self):
        return "{}.{}.{}.{}.{}".format(self.ticket_id,self.licence_no,self.parking_slot_id,self.hourly_price,self.start_time)
