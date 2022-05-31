from ast import Constant
import math
from datetime import datetime
from uuid import uuid1
from exception.api_response import ParkingServiceException
from models.constants import TicketStatus
from models.parking.parking_slot import ParkingSlot
from models.parking.ticket import ReservationTicket
from models.payment.payment import Payment
from models.vehicle.vehicle import Vehicle
from repository.memory import DB
from queue import PriorityQueue
from models.constants import VehicleType, TicketStatus

db = DB()
db.vehicle_price_table["four"] = 4
db.vehicle_price_table["two"] = 2

class ParkingService:
    """System : ParkingRow"""

    def __init__(self, available_slots:int, payment: Payment):
        
        self.available_slots = available_slots
        self.parking_slots = self._create_slots(available_slots)
        self.payment = payment # obj 
    
    @staticmethod
    def _create_slots(available_slots):
        parking_slots_q = PriorityQueue() 

        for temp_id in range(1, available_slots+1):
            slot = ParkingSlot(slot_id=temp_id)
            parking_slots_q.put((temp_id, slot))
        
        return parking_slots_q

    def _get_nearest_slot(self):
        id, slot = self.parking_slots.get()
        return slot

    def _update_nearest_slot(self, slot):
        self.parking_slots.put((slot._slot_id, slot))

    def _is_slot_available(self):
        return self.available_slots!=0
    
    def _validate_ticket(self, ticket_id):
        ticket = db.ticket_table.get(ticket_id)
        return True if ticket!=None else False

    def _is_vehicle_parked(self, licence_no):
        ticket_list = db.get_tickes_by_licence(licence_no)
        is_parked = False
        for ticket in ticket_list:
            if ticket.ticket_status == TicketStatus.RESERVED.value:
                is_parked = True
                break
        return is_parked

    def _get_hourly_price(self, vehicle_type):
        return db.vehicle_price_table[vehicle_type]

    def get_ticket(self, licence_no:str, contact_no:str, vehicle_type: str):
        if self._is_slot_available():
            if self._is_vehicle_parked(licence_no):
                raise ParkingServiceException("Vehicle Already Parked")
                
            # register vehicle 
            vehicle_id = str(uuid1())
            vehicle = Vehicle(vehicle_id, licence_no, contact_no, VehicleType(vehicle_type))
            db.vehicle_table[vehicle_id] = vehicle
            
            # assign slot
            slot = self._get_nearest_slot()
            slot.is_reserved = True
            slot.vehicle_id = vehicle_id
            db.parking_slot_table[slot._slot_id] = slot
            
            # initiate ticket
            ticket_id = str(uuid1())
            hourly_price = self._get_hourly_price(vehicle_type)
            ticket = ReservationTicket(parking_slot_id=slot._slot_id, licence_no=licence_no, ticket_id=ticket_id, hourly_price=hourly_price)
            db.ticket_table[ticket_id]=ticket
            self.available_slots -= 1
            return ticket
        else:
            raise ParkingServiceException("Parking Slot Not Available")
        
    def get_vehicle_history(self, licence_no):
        vehicle_parking_history =  db.get_tickes_by_licence(licence_no)
        if vehicle_parking_history == None:
            raise ParkingServiceException("Vehicle was never Parked.")
        return vehicle_parking_history

    def get_all_vehicle_history(self):
        history_data = [ticket for _, ticket in db.ticket_table.items()]
        history_data.sort(key=lambda x: x.start_time, reverse=True)
        return history_data

    def checkout_vehicle(self, ticket_id):
        """
            Update slot status
            Update Ticket History
        """
        if self._validate_ticket(ticket_id):
            ticket = db.ticket_table[ticket_id]
            # Get Slot & Vehicle
            slot = db.parking_slot_table[ticket.parking_slot_id]

            # Calculate Total Price
            ticket.end_time = datetime.now()
            total_hours = math.ceil((ticket.end_time - ticket.start_time).total_seconds()/3600)
            ticket.total_price = total_hours * ticket.hourly_price
            
            # initiate payment
            is_paid = self.payment.transact(ticket.total_price)
            if is_paid == True:
                # we can update the slot status
                slot._is_reserved = False
                slot._vehicle_id = None
                db.parking_slot_table[ticket.parking_slot_id] = slot

                # update history
                del db.ticket_table[ticket_id]
                ticket.ticket_status = TicketStatus.PAID.value
                db.ticket_table[ticket_id]= ticket

                # update nearest slot
                self._update_nearest_slot(slot)
                self.available_slots = self.available_slots+1
                return ticket
            else:
                raise ParkingServiceException("Payment Failed, Please Retry")
        else:
            raise ParkingServiceException("Not a valid Ticket")
    