from ast import Assert
from unittest import TestCase
import unittest
from exception.api_response import ParkingServiceException
from models.payment.basic_payment import BasicPayment
from services.parking_service import ParkingService

class TestParkingService(TestCase):

    def test_park_a_vehicle(self):
        """
        Test parking a car
        While parking price and endtime will be null
        """
        service = ParkingService(2, payment = BasicPayment())
        ticket = service.get_ticket("UPSE70210", 8658823367, "four")

        self.assertIsNotNone(ticket)
        self.assertIsNotNone(ticket.ticket_id)
        self.assertIsNone(ticket.end_time)
        self.assertIsNone(ticket.total_price)
        

    def test_check_out_vehicle(self):
        """
        Test checking out a car
        While checking out a car endtime and total price should not be null
        """
        service = ParkingService(2, payment = BasicPayment())
        ticket = service.get_ticket("UPSE70212", 8658823367, "four")
        self.assertIsNotNone(ticket)

        checkout = service.checkout_vehicle(ticket.ticket_id)
        self.assertIsNotNone(checkout.end_time)
        self.assertIsNotNone(checkout.total_price)

    def test_ticket_history(self):
        """
        Test Parking History
        History should not be none
        """
        service = ParkingService(2, payment = BasicPayment())
        ticket = service.get_ticket("UPSE70255", 8658823367, "four")
        self.assertIsNotNone(ticket)

        history = service.get_vehicle_history("UPSE70255")
        self.assertIsNotNone(history)

    
    def test_parking_slot_full(self):
        """
        Test Parking lot full 
        Throws expection when parking is full
        """
        service = ParkingService(2, payment = BasicPayment())

        ticket1 = service.get_ticket("UPSE70211", 8658823367, "four")
        ticket2 = service.get_ticket("UPSE37022", 8658823367, "four")
        
        with self.assertRaises(ParkingServiceException) as ex:
            ticket3 = service.get_ticket("UPSE27023", 8658823367, "four")

        self.assertEqual(
            'Parking Slot Not Available',
            str(ex.exception)
        )


    def test_vehicle_already_parked(self):
        """
        Test Vehicle already parked 
        Throws expection that vehicle is already parked
        """
        service = ParkingService(2, payment = BasicPayment())
        ticket1 = service.get_ticket("UPSE27023", 8658823367, "four")
                
        with self.assertRaises(ParkingServiceException) as ex:
            ticket2 = service.get_ticket("UPSE27023", 8658823367, "four")

        self.assertEqual(
            'Vehicle Already Parked',
            str(ex.exception)
        )
