import unittest
from unittest.mock import patch, mock_open
import builtins
import sys

# Предположим, что все функции и переменные импортированы из основного модуля
# from bank_app import account, hash_password, create_account, deposit_money, withdraw_money, handle_transaction, set_threshold, apply_transactions, filter_by_amount, delayed_payment

class TestBankApp(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='user\n30\nlogin\npassword\n123456789\n100.0\n0.0\n')
    def test_load_account_data(self, mock_file):
        account_data = load_account_data('login')
        self.assertEqual(account_data['full_name'], 'user')
        self.assertEqual(account_data['age'], 30)
        self.assertEqual(account_data['login'], 'login')
        self.assertEqual(account_data['password'], 'password')
        self.assertEqual(account_data['password_hash'], '123456789')
        self.assertEqual(account_data['balance'], 100.0)
        self.assertEqual(account_data['threshold'], 0.0)
        self.assertEqual(account_data['transactions'], [])
        self.assertEqual(account_data['pending_payments'], [])

    def test_hash_password(self):
        password = "password123"
        hashed_password = hash_password(password)
        self.assertTrue(hashed_password)
        self.assertNotEqual(password, hashed_password)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_account_data(self, mock_file):
        account_data = {
            'full_name': 'user',
            'age': 30,
            'login': 'login',
            'password': 'password',
            'password_hash': '123456789',
            'balance': 100.0,
            'threshold': 0.0,
            'transactions': [{'comment': 'Test', 'amount': 10}],
            'pending_payments': [{'recipient_login': 'recipient', 'amount': 50}]
        }
        save_account_data(account_data)
        mock_file().write.assert_called()

    @patch('builtins.input', side_effect=['user', '1994', 'login', 'password'])
    @patch('builtins.open', new_callable=mock_open)
    def test_create_account(self, mock_file, mock_input):
        message = create_account_cli()
        self.assertIn("Создан аккаунт", message)

    @patch('builtins.input', side_effect=['login', '100'])
    @patch('builtins.open', new_callable=mock_open, read_data='user\n30\nlogin\npassword\n123456789\n100.0\n0.0\n')
    def test_deposit_money_cli(self, mock_file, mock_input):
        balance = deposit_money_cli()
        self.assertEqual(balance, 200.0)

    @patch('builtins.input', side_effect=['login', 'password', '50'])
    @patch('builtins.open', new_callable=mock_open, read_data='user\n30\nlogin\npassword\n123456789\n100.0\n0.0\n')
    def test_withdraw_money_cli(self, mock_file, mock_input):
        balance = withdraw_money_cli()
        self.assertEqual(balance, 50.0)

    @patch('builtins.input', side_effect=['login'])
    @patch('builtins.open', new_callable=mock_open, read_data='user\n30\nlogin\npassword\n123456789\n100.0\n0.0\n')
    def test_show_balance_cli(self, mock_file, mock_input):
        balance = show_balance_cli()
        self.assertEqual(balance, 100.0)

    @patch('builtins.input', side_effect=['login', 'Test transaction', '10'])
    @patch('builtins.open', new_callable=mock_open, read_data='user\n30\nlogin\npassword\n123456789\n100.0\n0.0\n')
    def test_handle_transaction_cli(self, mock_file, mock_input):
        transactions = handle_transaction_cli()
        self.assertEqual(transactions, [{'comment': 'Test transaction', 'amount': 10}])

    @patch('builtins.input', side_effect=['login', '50'])
    @patch('builtins.open', new_callable=mock_open, read_data='user\n30\nlogin\npassword\n123456789\n100.0\n0.0\n')
    def test_set_threshold_cli(self, mock_file, mock_input):
        threshold = set_threshold_cli()
        self.assertEqual(threshold, 50.0)

    @patch('builtins.input', side_effect=['login'])
    @patch('builtins.open', new_callable=mock_open, read_data='user\n30\nlogin\npassword\n123456789\n100.0\n50.0\nTest transaction:10\n')
    def test_apply_transactions_cli(self, mock_file, mock_input):
        balance = apply_transactions_cli()
        self.assertEqual(balance, 110.0)

    @patch('builtins.input', side_effect=['login', '10'])
    @patch('builtins.open', new_callable=mock_open, read_data='user\n30\nlogin\npassword\n123456789\n100.0\n0.0\nTest transaction:10\n')
    def test_filter_by_amount_cli(self, mock_file, mock_input):
        filtered_transactions = filter_by_amount_cli()
        self.assertEqual(filtered_transactions, [{'comment': 'Test transaction', 'amount': 10}])

    @patch('builtins.input', side_effect=['sender', 'password', 'recipient', '50'])
    @patch('builtins.open', new_callable=mock_open, read_data='user\n30\nsender\npassword\n123456789\n100.0\n0.0\n')
    def test_delayed_payment_cli(self, mock_file, mock_input):
        result = delayed_payment_cli()
        self.assertIn("Платеж успешно выполнен.", result)


if __name__ == '__main__':
    unittest.main()
