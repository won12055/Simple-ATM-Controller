class Account:
    def __init__(self, account_id: str, balance: int = 0):
        self.account_id = account_id
        self.balance = balance
    
    def deposit(self, amount: int):
        if amount <= 0:
            raise ValueError('Deposit must be positive.')
        self.balance += amount

    def withdraw(self, amount: int):
        if amount <= 0:
            raise ValueError('Withdrawal must be positive.')
        if amount > self.balance:
            raise ValueError('Insufficient funds.')
        self.balance -= amount

    def get_balance(self):
        return self.balance