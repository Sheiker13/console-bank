import unittest
from main import *

class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        global account
        account = {'full_name': 'Test User', 'age': 25, 'login': 'testuser', 'password': 'testpass',
                   'password_hash': hash_password('testpass'), 'balance': 100.0, 'threshold': 50.0,
                   'transactions': [], 'pending_payments': []}

    def test_hash_password(self):
        self.assertEqual(hash_password('testpass'), '9171164826599050')

    def test_create_account(self):
        account['full_name'] = 'Test User'
        account['age'] = 25
        account['login'] = 'testuser'
        account['password'] = 'testpass'
        account['password_hash'] = hash_password('testpass')
        save_password_hash()
        save_to_file()
        loaded_account = load_account_data('testuser')
        self.assertEqual(account, loaded_account)

    def test_deposit_money(self):
        load_from_file('testuser')
        account['balance'] = 100.0
        amount = 50.0
        account['balance'] += amount
        save_to_file()
        self.assertEqual(account['balance'], 150.0)

    def test_withdraw_money(self):
        load_from_file('testuser')
        account['balance'] = 100.0
        amount = 50.0
        account['balance'] -= amount
        save_to_file()
        self.assertEqual(account['balance'], 50.0)

    def test_handle_transaction(self):
        load_from_file('testuser')
        transaction = {'comment': 'Test transaction', 'amount': 30.0}
        account['transactions'].append(transaction)
        save_to_file()
        self.assertIn(transaction, account['transactions'])

    def test_set_threshold(self):
        load_from_file('testuser')
        new_threshold = 100.0
        account['threshold'] = new_threshold
        save_to_file()
        self.assertEqual(account['threshold'], new_threshold)

    def test_apply_transactions(self):
        load_from_file('testuser')
        account['transactions'] = [{'comment': 'Transaction 1', 'amount': 40.0}, {'comment': 'Transaction 2', 'amount': 60.0}]
        account['threshold'] = 50.0
        apply_transactions()
        self.assertEqual(account['balance'], 140.0)  # 100 (initial balance) + 40 (first transaction applied)

    def test_show_transaction_stats(self):
        load_from_file('testuser')
        account['transactions'] = [{'comment': 'Transaction 1', 'amount': 40.0}, {'comment': 'Transaction 2', 'amount': 40.0}, {'comment': 'Transaction 3', 'amount': 60.0}]
        stats = show_transaction_stats()
        self.assertEqual(stats, {40.0: 2, 60.0: 1})

    def test_filter_by_amount(self):
        load_from_file('testuser')
        account['transactions'] = [{'comment': 'Transaction 1', 'amount': 40.0}, {'comment': 'Transaction 2', 'amount': 60.0}]
        filtered_transactions = list(filter_by_amount())
        self.assertEqual(filtered_transactions, [{'comment': 'Transaction 2', 'amount': 60.0}])

    def test_delayed_payment(self):
        load_from_file('testuser')
        recipient_account = {'full_name': 'Recipient User', 'age': 25, 'login': 'recipientuser', 'password': 'recpass', 'password_hash': hash_password('recpass'), 'balance': 50.0, 'threshold': 50.0, 'transactions': [], 'pending_payments': []}
        save_account_data(recipient_account)
        account['balance'] = 100.0
        amount = 30.0
        account['balance'] -= amount
        save_to_file()
        recipient_data = load_account_data('recipientuser')
        recipient_data['balance'] += amount
        save_account_data(recipient_data)
        self.assertEqual(recipient_data['balance'], 80.0)

    def test_process_pending_payments(self):
        load_from_file('testuser')
        account['balance'] = 100.0
        account['pending_payments'] = [{'recipient_login': 'recipientuser', 'amount': 30.0}]
        process_pending_payments()
        recipient_data = load_account_data('recipientuser')
        self.assertEqual(recipient_data['balance'], 80.0)  # Assuming recipient had an initial balance of 50.0

if __name__ == '__main__':
    unittest.main()
