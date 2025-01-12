from atm.user import User, AccountType

class MockBankAPI:
    def __init__(self):
        self.users = {
            '1234567890': User(
                card_number='123456789012',
                pin='1234',
                accounts={
                    AccountType.CHECKING: 1000,
                    AccountType.SAVINGS: 500
                }
            )
        }

    def verify_pin(self, card_number: str, pin: str) -> bool:
        user = self.users.get(card_number)
        if user and user.verify_pin(pin):
            return True
    
    def get_accounts(self, card_number: str) -> dict:
        user = self.users.get(card_number)
        if user:
            return user.get_accounts()
        return {}
    
    def update_balance(self, card_number: str, account_type: str, new_balance: int):
        user = self.users.get(card_number)
        if user:
            user.update_balance(account_type, new_balance)
        else:
            raise ValueError(f"User with card number '{card_number}' does not exist.")
