
from models.payment.payment import Payment


class BasicPayment(Payment):
    
    def transact(self, amount):
        # TODO : transaction_id, Status
        return True
