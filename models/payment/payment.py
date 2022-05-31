from abc import abstractmethod


class Payment:
    def __init__(self):
        pass

    @abstractmethod
    def transact(self, amount):
        pass
