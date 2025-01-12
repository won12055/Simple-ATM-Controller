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
        accounts_repr = {account_type.name: balance for account_type, balance in self.accounts.items()}
        return f"User(card_number={self.card_number}, accounts={accounts_repr})"