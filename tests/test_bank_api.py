import unittest
from atm.bank_api import MockBankAPI
from atm.user import AccountType

class TestMockBankAPI(unittest.TestCase):
    def setUp(self):
        self.bank_api = MockBankAPI()

    def test_verify_pin_correct(self):
        self.assertTrue(self.bank_api.verify_pin('123456789012', '1234'))

    def test_verify_pin_incorrect(self):
        self.assertFalse(self.bank_api.verify_pin('123456789012', '0000'))

    def test_verify_pin_nonexistent_card(self):
        self.assertFalse(self.bank_api.verify_pin('000000000000', '1234'))

    def test_get_accounts_valid_card(self):
        accounts = self.bank_api.get_accounts('123456789012')
        expected_accounts = {
            AccountType.CHECKING: 1000,
            AccountType.SAVINGS: 500
        }
        self.assertEqual(accounts, expected_accounts)

    def test_get_accounts_invalid_card(self):
        accounts = self.bank_api.get_accounts('000000000000')
        self.assertEqual(accounts, {})

    def test_update_balance_valid(self):
        self.bank_api.update_balance('123456789012', AccountType.CHECKING, 1500)
        accounts = self.bank_api.get_accounts('123456789012')
        self.assertEqual(accounts[AccountType.CHECKING], 1500)

    def test_update_balance_invalid_account_type(self):
        with self.assertRaises(ValueError):
            self.bank_api.update_balance('123456789012', AccountType('investment'), 1000)

    def test_update_balance_nonexistent_user(self):
        with self.assertRaises(ValueError):
            self.bank_api.update_balance('000000000000', AccountType.CHECKING, 1000)
