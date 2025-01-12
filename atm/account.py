from atm.user import AccountType

class Account:
    def __init__(self, account_id: AccountType, balance: int = 0):
        self.account_id = account_id
        self.balance = balance
        self.transaction_history = []  

    def deposit(self, amount: int):
        if amount <= 0:
            raise ValueError('Deposit must be positive.')
        self.balance += amount
        self.transaction_history.append(('deposit', amount))

    def withdraw(self, amount: int):
        if amount <= 0:
            raise ValueError('Withdrawal must be positive.')
        if amount > self.balance:
            raise ValueError('Insufficient funds.')
        self.balance -= amount
        self.transaction_history.append(('withdraw', amount))

    def get_balance(self) -> int:
        return self.balance

    def get_transaction_history(self) -> list:
        return self.transaction_history