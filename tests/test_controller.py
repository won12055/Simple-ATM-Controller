import unittest
from atm.bank_api import MockBankAPI
from atm.controller import ATMController
from atm.user import AccountType

class TestATMController(unittest.TestCase):
    def setUp(self):
        self.bank_api = MockBankAPI()
        self.atm = ATMController(self.bank_api)

    def test_insert_card_success(self):
        self.atm.insert_card('123456789012')
        self.assertTrue(self.atm.card_inserted)
        self.assertEqual(self.atm.card_number, '123456789012')

    def test_insert_card_already_inserted(self):
        self.atm.insert_card('123456789012')
        with self.assertRaises(ValueError):
            self.atm.insert_card('098765432109')

    def test_enter_pin_success(self):
        self.atm.insert_card('123456789012')
        result = self.atm.enter_pin('1234')
        self.assertTrue(result)
        self.assertTrue(self.atm.authenticated)
        self.assertEqual(self.atm.accounts, {
            AccountType.CHECKING: 1000,
            AccountType.SAVINGS: 500
        })

    def test_enter_pin_incorrect(self):
        self.atm.insert_card('123456789012')
        result = self.atm.enter_pin('0000')
        self.assertFalse(result)
        self.assertFalse(self.atm.authenticated)
        self.assertEqual(self.atm.pin_attempts, 1)

    def test_enter_pin_max_attempts(self):
        self.atm.insert_card('123456789012')
        for i in range(3):
            result = self.atm.enter_pin('0000')
            self.assertFalse(result)
        self.assertFalse(self.atm.card_inserted)
        self.assertFalse(self.atm.authenticated)

    def test_select_account_success(self):
        self.atm.insert_card('123456789012')
        self.atm.enter_pin('1234')
        self.atm.select_account(AccountType.CHECKING)
        self.assertIsNotNone(self.atm.selected_account)
        self.assertEqual(self.atm.selected_account.account_id, AccountType.CHECKING)
        self.assertEqual(self.atm.selected_account.balance, 1000)

    def test_select_account_not_authenticated(self):
        self.atm.insert_card('123456789012')
        with self.assertRaises(Exception):
            self.atm.select_account(AccountType.CHECKING)

    def test_select_account_invalid_account_type(self):
        self.atm.insert_card('123456789012')
        self.atm.enter_pin('1234')
        with self.assertRaises(ValueError):
            self.atm.select_account(AccountType('investment'))

    def test_get_balance_success(self):
        self.atm.insert_card('123456789012')
        self.atm.enter_pin('1234')
        self.atm.select_account(AccountType.SAVINGS)
        balance = self.atm.get_balance()
        self.assertEqual(balance, 500)

    def test_get_balance_no_account_selected(self):
        self.atm.insert_card('123456789012')
        self.atm.enter_pin('1234')
        with self.assertRaises(Exception):
            self.atm.get_balance()

    def test_deposit_success(self):
        self.atm.insert_card('123456789012')
        self.atm.enter_pin('1234')
        self.atm.select_account(AccountType.CHECKING)
        self.atm.deposit(500)
        self.assertEqual(self.atm.selected_account.balance, 1500)
        # Verify via MockBankAPI
        accounts = self.bank_api.get_accounts('123456789012')
        self.assertEqual(accounts[AccountType.CHECKING], 1500)

    def test_deposit_no_account_selected(self):
        self.atm.insert_card('123456789012')
        self.atm.enter_pin('1234')
        with self.assertRaises(Exception):
            self.atm.deposit(500)

    def test_withdraw_success(self):
        self.atm.insert_card('123456789012')
        self.atm.enter_pin('1234')
        self.atm.select_account(AccountType.SAVINGS)
        self.atm.withdraw(200)
        self.assertEqual(self.atm.selected_account.balance, 300)
        # Verify via MockBankAPI
        accounts = self.bank_api.get_accounts('123456789012')
        self.assertEqual(accounts[AccountType.SAVINGS], 300)

    def test_withdraw_insufficient_funds(self):
        self.atm.insert_card('123456789012')
        self.atm.enter_pin('1234')
        self.atm.select_account(AccountType.SAVINGS)
        with self.assertRaises(ValueError):
            self.atm.withdraw(600)

    def test_withdraw_no_account_selected(self):
        self.atm.insert_card('123456789012')
        self.atm.enter_pin('1234')
        with self.assertRaises(Exception):
            self.atm.withdraw(100)

    def test_eject_card_success(self):
        self.atm.insert_card('123456789012')
        self.atm.eject_card()
        self.assertFalse(self.atm.card_inserted)
        self.assertIsNone(self.atm.card_number)
        self.assertFalse(self.atm.authenticated)
        self.assertEqual(self.atm.accounts, {})
        self.assertIsNone(self.atm.selected_account)

    def test_eject_card_no_card_inserted(self):
        with self.assertRaises(Exception):
            self.atm.eject_card()
