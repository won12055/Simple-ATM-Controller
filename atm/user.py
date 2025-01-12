from enum import Enum

class AccountType(Enum):
    CHECKING = 'checking',
    SAVINGS = 'savings'

class User:
    def __init__(self, card_number: str, pin: str, accounts: dict):
        self.card_number = card_number
        self.pin = pin
        self.accounts = accounts 

    def verify_pin(self, pin: str) -> bool:
        return self.pin == pin
    
    def get_accounts(self) -> dict:
        return self.accounts
    
    def update_balance(self, account_type: str, new_balance: int):
        if account_type in self.accounts:
            self.accounts[account_type] = new_balance
        else:
            raise ValueError(f"Account type '{account_type}' does not exist for this user.")