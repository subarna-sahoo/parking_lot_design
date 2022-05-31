from unittest import TestCase
import unittest
from models.payment.basic_payment import BasicPayment
from services.parking_service import ParkingService

class TestParkingService(TestCase):
    def test_fill_slot_parking_slot_available(self):
        s = ParkingService(2, payment = BasicPayment())

        ticket1 = s.get_ticket("UPSE7021", 8658823367, "four")
        ticket2 = s.get_ticket("UPSE37022", 8658823367, "four")
        ticket3 = s.get_ticket("UPSE27023", 8658823367, "four")
        ticket4 = s.get_ticket("UPSE27024", 8658823367, "four")
        s.checkout_vehicle(ticket1.ticket_id)
        ticket4 = s.get_ticket("UPSE27024", 8658823367, "four")
        print(ticket4)
