import unittest
from atm.account import Account
from atm.user import AccountType

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(AccountType.CHECKING, 1000)

    def test_account_initialization(self):
        self.assertEqual(self.account.account_id, AccountType.CHECKING)
        self.assertEqual(self.account.balance, 1000)
        self.assertEqual(self.account.transaction_history, [])

    def test_deposit_positive_amount(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)
        self.assertIn(('deposit', 500), self.account.transaction_history)

    def test_deposit_negative_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100)

    def test_deposit_zero_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    def test_withdraw_positive_amount(self):
        self.account.withdraw(300)
        self.assertEqual(self.account.balance, 700)
        self.assertIn(('withdraw', 300), self.account.transaction_history)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1500)

    def test_withdraw_negative_amount(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-100)

    def test_withdraw_zero_amount(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0)

    def test_get_balance(self):
        balance = self.account.get_balance()
        self.assertEqual(balance, 1000)

    def test_get_transaction_history(self):
        self.account.deposit(500)
        self.account.withdraw(200)
        history = self.account.get_transaction_history()
        expected_history = [
            ('deposit', 500),
            ('withdraw', 200)
        ]
        self.assertEqual(history, expected_history)