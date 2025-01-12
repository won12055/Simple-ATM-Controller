from atm.bank_api import MockBankAPI
from atm.controller import ATMController
from atm.user import AccountType

def main():
    bank_api = MockBankAPI()
    atm = ATMController(bank_api)

    try:
        atm.insert_card('123456789012')

        if atm.enter_pin('1234'):
            atm.select_account(AccountType.CHECKING)

            balance = atm.get_balance()
            print(f"Balance: ${balance}")

            atm.deposit(500)

            atm.withdraw(200)

            balance = atm.get_balance()
            print(f"Balance after transactions: ${balance}")

        atm.eject_card()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()