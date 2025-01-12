from atm.bank_api import MockBankAPI
from atm.user import AccountType
from atm.account import Account

class ATMController:
    def __init__(self, bank_api: MockBankAPI, max_pin_attempts: int = 3):
        self.bank_api = bank_api
        self.card_inserted = False
        self.card_number = None
        self.authenticated = False
        self.accounts = {}
        self.selected_account = None
        self.pin_attempts = 0
        self.max_pin_attempts = max_pin_attempts

    def insert_card(self, card_number: str):
        if self.card_inserted:
            raise ValueError('Card already inserted.')
        self.card_inserted = True
        self.card_number = card_number
        print(f"Card {card_number} inserted.")

    def enter_pin(self, pin: str) -> bool:
        if not self.card_inserted:
            raise Exception("No card inserted.")
        if self.authenticated:
            print("Already authenticated.")
            return True
        self.authenticated = self.bank_api.verify_pin(self.card_number, pin)
        if self.authenticated:
            self.accounts = self.bank_api.get_accounts(self.card_number)
            self.pin_attempts = 0
            print("PIN verified successfully.")
            return True
        else:
            self.pin_attempts += 1
            attempts_left = self.max_pin_attempts - self.pin_attempts
            print(f"Invalid PIN. {attempts_left} attempts left.")
            if self.pin_attempts >= self.max_pin_attempts:
                self.eject_card()
            return False

    def select_account(self, account_type: AccountType):
        if not self.authenticated:
            raise Exception("Not authenticated.")
        if account_type not in self.accounts:
            raise ValueError(f"Account type '{account_type.value}' does not exist for this user.")
        self.selected_account = Account(account_type, self.accounts[account_type])
        print(f"Selected account: {account_type.value}")

    def get_balance(self) -> int:
        self._ensure_account_selected()
        balance = self.selected_account.get_balance()
        print(f"Current balance: ${balance}")
        return balance
    
    def deposit(self, amount: int):
        self._ensure_account_selected()
        self.selected_account.deposit(amount)
        self.bank_api.update_balance(self.card_number, self.selected_account.account_id, self.selected_account.balance)
        print(f"${amount} deposited. New balance: ${self.selected_account.balance}")

    def withdraw(self, amount: int):
        self._ensure_account_selected()
        self.selected_account.withdraw(amount)
        self.bank_api.update_balance(self.card_number, self.selected_account.account_id, self.selected_account.balance)
        print(f"${amount} withdrawn. New balance: ${self.selected_account.balance}")    

    def eject_card(self):
        if not self.card_inserted:
            raise Exception("No card to eject.")
        print(f"Card {self.card_number} ejected.")
        self.card_inserted = False
        self.card_number = None
        self.authenticated = False
        self.accounts = {}
        self.selected_account = None

    def _ensure_account_selected(self):
        if not self.selected_account:
            raise Exception("No account selected.")