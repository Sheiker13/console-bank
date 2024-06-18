import unittest
from main import (create_account, deposit_money, withdraw_money, handle_transaction,
                       set_threshold, apply_transactions, show_transaction_stats, filter_by_amount,
                       delayed_payment, account)


class TestBankingApp(unittest.TestCase):

    def setUp(self):
        account.update(
            {'full_name': '', 'age': 0, 'login': '', 'password': '', 'password_hash': '', 'balance': 0, 'threshold': 0,
             'transactions': [], 'pending_payments': []})

    def test_create_account(self):
        response = create_account('John Doe', 1980, 'johndoe', 'password123')
        self.assertIn('Создан аккаунт: John Doe 44 лет, Логин: johndoe', response)

    def test_deposit_money(self):
        create_account('John Doe', 1980, 'johndoe', 'password123')
        balance = deposit_money('johndoe', 500)
        self.assertEqual(balance, 500)

    def test_withdraw_money(self):
        create_account('John Doe', 1980, 'johndoe', 'password123')
        deposit_money('johndoe', 500)
        balance = withdraw_money('johndoe', 'password123', 200)
        self.assertEqual(balance, 300)

    def test_handle_transaction(self):
        create_account('John Doe', 1980, 'johndoe', 'password123')
        deposit_money('johndoe', 500)
        transactions = handle_transaction('johndoe', 'Test Transaction', 100)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['comment'], 'Test Transaction')
        self.assertEqual(transactions[0]['amount'], 100)

    def test_set_threshold(self):
        create_account('John Doe', 1980, 'johndoe', 'password123')
        threshold = set_threshold('johndoe', 300)
        self.assertEqual(threshold, 300)

    def test_apply_transactions(self):
        create_account('John Doe', 1980, 'johndoe', 'password123')
        deposit_money('johndoe', 500)
        set_threshold('johndoe', 300)
        handle_transaction('johndoe', 'Test Transaction 1', 100)
        handle_transaction('johndoe', 'Test Transaction 2', 400)
        balance = apply_transactions('johndoe')
        self.assertEqual(balance, 600)

    def test_show_transaction_stats(self):
        create_account('John Doe', 1980, 'johndoe', 'password123')
        handle_transaction('johndoe', 'Test Transaction 1', 100)
        handle_transaction('johndoe', 'Test Transaction 2', 100)
        stats = show_transaction_stats('johndoe')
        self.assertEqual(stats[100], 2)

    def test_filter_by_amount(self):
        create_account('John Doe', 1980, 'johndoe', 'password123')
        handle_transaction('johndoe', 'Test Transaction 1', 100)
        handle_transaction('johndoe', 'Test Transaction 2', 400)
        filtered_transactions = filter_by_amount('johndoe', 200)
        self.assertEqual(len(filtered_transactions), 1)
        self.assertEqual(filtered_transactions[0]['amount'], 400)

    def test_delayed_payment(self):
        create_account('John Doe', 1980, 'johndoe', 'password123')
        deposit_money('johndoe', 500)
        create_account('Jane Doe', 1985, 'janedoe', 'password456')
        response = delayed_payment('johndoe', 'password123', 'janedoe', 200)
        self.assertEqual(response, "Платеж успешно выполнен.")


if __name__ == '__main__':
    unittest.main()
