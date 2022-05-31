class DB:
    def __init__(self):
        self.parking_slot_table = {}            # slot_id       ->> slot_details
        self.payment_table = {}                 # payment_id    ->> payment_details
        self.vehicle_price_table = {}           # vehicle_type  ->> price_details | manually
        self.vehicle_table = {}                 # vehicle_id    ->> vehicle_details
        self.ticket_table = {}                  # ticket_id    ->> []veichel_ticket_history  | 



    def get_tickes_by_licence(self, inp_licence_no):
        """We will create index on licence_no"""
        tickets = []
        for ticket_id in self.ticket_table:
            ticket = self.ticket_table[ticket_id]
            if ticket.licence_no == inp_licence_no:
                tickets.append(ticket)
        return tickets
