import unittest
from atm.user import User, AccountType

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(
            card_number='123456789012',
            pin='1234',
            accounts={
                AccountType.CHECKING: 1000,
                AccountType.SAVINGS: 500
            }
        )

    def test_user_initialization(self):
        self.assertEqual(self.user.card_number, '123456789012')
        self.assertEqual(self.user.pin, '1234')
        self.assertEqual(self.user.accounts[AccountType.CHECKING], 1000)
        self.assertEqual(self.user.accounts[AccountType.SAVINGS], 500)

    def test_user_repr(self):
        expected_repr = "User(card_number=123456789012, accounts={'CHECKING': 1000, 'SAVINGS': 500})"
        self.assertEqual(repr(self.user), expected_repr)


