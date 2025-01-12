from enum import Enum

class AccountType(Enum):
    CHECKING = 'checking'
    SAVINGS = 'savings'

class User:
    def __init__(self, card_number: str, pin: str, accounts: dict):
        self.card_number = card_number
        self.pin = pin
        self.accounts = accounts 

    def __repr__(self):
            return f"User(card_number={self.card_number}, accounts={self.accounts})"
