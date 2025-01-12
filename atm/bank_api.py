from atm.user import User, AccountType

class MockBankAPI:
    def __init__(self):
        self.users = {
            '123456789012': User(  
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
        if user and user.pin == pin:
            return True
        return False

    def get_accounts(self, card_number: str) -> dict:
        user = self.users.get(card_number)
        if user:
            return user.accounts
        return {}

    def update_balance(self, card_number: str, account_type: AccountType, new_balance: int):
        user = self.users.get(card_number)
        if user:
            if account_type in user.accounts:
                user.accounts[account_type] = new_balance
            else:
                raise ValueError(f"Account type '{account_type.value}' does not exist for this user.")
        else:
            raise ValueError(f"User with card number '{card_number}' does not exist.")