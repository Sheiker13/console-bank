import sys

account = {'full_name': '', 'age': 0, 'password': '', 'password_hash': '', 'balance': 0, 'threshold': 0, 'transactions': []}

def log_error(err_msg):
    print(f"ERROR: {err_msg}")

def hash_password(password):
    try:
        sum_codes = sum(ord(char) for char in password)
        product_codes = 1
        for char in password:
            product_codes *= ord(char)
        prime_number = 1234001651
        sum_hash = sum_codes % prime_number
        product_hash = product_codes % prime_number
        return f"{sum_hash}{product_hash}"
    except Exception as e:
        log_error(f"Error hashing password: {e}")
        return ""

def save_password_hash():
    try:
        with open("passwordhash.txt", "w") as file_out:
            file_out.write(account['password_hash'])
    except Exception as e:
        log_error(f"Ошибка при сохранении хеша пароля: {e}")

def load_password_hash():
    try:
        with open("passwordhash.txt", "r") as file_in:
            account['password_hash'] = file_in.read().strip()
    except FileNotFoundError:
        log_error("Файл хеша пароля не найден.")
    except Exception as e:
        log_error(f"Ошибка при загрузке хеша пароля: {e}")

def create_account():
    try:
        account['full_name'] = input("Введите Ф.И.О: ")
        birth_year = int(input("Введите год рождения: "))
        account['age'] = 2024 - birth_year
        password = input("Введите пароль: ")
        account['password'] = password
        account['password_hash'] = hash_password(password)
        save_password_hash()
        print(f"Создан аккаунт: {account['full_name']} {account['age']} лет")
        print("Аккаунт успешно зарегистрирован!")
    except Exception as e:
        log_error(e)

def deposit_money():
    try:
        amount = float(input("Введите сумму пополнения: "))
        if amount > 0:
            account['balance'] += amount
            print("Счёт успешно пополнен на сумму:", amount)
        else:
            print("Сумма должна быть больше нуля.")
    except ValueError:
        log_error("Неверный формат суммы, должно быть число.")

def withdraw_money():
    try:
        password = input("Введите пароль: ")
        if hash_password(password) == account['password_hash']:
            amount = float(input("Введите сумму для снятия: "))
            if amount > account['balance']:
                print("Недостаточно средств на счету.")
            elif amount <= 0:
                print("Сумма должна быть больше нуля.")
            else:
                account['balance'] -= amount
                print(f"Вы сняли {amount} с вашего счета.")
        else:
            print("Неверный пароль!")
    except ValueError:
        log_error("Ошибка при вводе суммы.")

def handle_transaction():
    try:
        comment = input("Введите комментарий для транзакции: ")
        amount = float(input("Введите сумму: "))
        transaction = {'comment': comment, 'amount': amount}
        account['transactions'].append(transaction)
        print(f"Транзакция добавлена. Комментарий: {comment}, сумма: {amount}")
    except ValueError:
        log_error("Ошибка при вводе данных транзакции.")

def set_threshold():
    try:
        threshold = float(input("Введите новый лимит транзакций: "))
        account['threshold'] = threshold
        print(f"Лимит транзакций установлен на: {threshold}")
    except ValueError:
        log_error("Ошибка при установке лимита. Введите число.")

def apply_transactions():
    try:
        new_transactions = []
        for transaction in account['transactions']:
            if transaction['amount'] <= account['threshold']:
                account['balance'] += transaction['amount']
                print(f"Транзакция на {transaction['amount']} применена.")
            else:
                new_transactions.append(transaction)
                print(f"Транзакция на {transaction['amount']} отклонена из-за лимита.")
        account['transactions'] = new_transactions
    except Exception as e:
        log_error(f"Ошибка при применении транзакций: {e}")

def show_transaction_stats():
    try:
        freq = {}
        for transaction in account['transactions']:
            amount = transaction['amount']
            if amount in freq:
                freq[amount] += 1
            else:
                freq[amount] = 1
        for amount, count in freq.items():
            print(f"Транзакций с суммой {amount}: {count}")
    except Exception as e:
        log_error(f"Ошибка при отображении статистики транзакций: {e}")

def filter_by_amount():
    try:
        filter_amount = float(input("Введите сумму для фильтрации: "))
        for transaction in account['transactions']:
            if transaction['amount'] >= filter_amount:
                yield transaction
    except ValueError:
        log_error("Неверный формат суммы, должно быть число.")
    except Exception as e:
        log_error(f"Ошибка при фильтрации транзакций: {e}")

def show_filtered_transactions():
    print("Фильтрация транзакций по заданной сумме:")
    filtered_transactions = filter_by_amount()
    for transaction in filtered_transactions:
        print(f"Транзакция: Комментарий - {transaction['comment']}, Сумма - {transaction['amount']}")

def save_to_file():
    try:
        with open("account_data.txt", "w") as file_out:
            file_out.write(f"{account['full_name']}\n")
            file_out.write(f"{account['age']}\n")
            file_out.write(f"{account['password']}\n")
            file_out.write(f"{account['password_hash']}\n")
            file_out.write(f"{account['balance']}\n")
            file_out.write(f"{account['threshold']}\n")
            for transaction in account['transactions']:
                file_out.write(f"{transaction['comment']}:{transaction['amount']}\n")
        print("Данные аккаунта сохранены.")
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def load_from_file():
    try:
        with open("account_data.txt", "r") as file_in:
            account['full_name'] = file_in.readline().strip()
            account['age'] = int(file_in.readline().strip())
            account['password'] = file_in.readline().strip()
            account['password_hash'] = file_in.readline().strip()
            account['balance'] = float(file_in.readline().strip())
            account['threshold'] = float(file_in.readline().strip())
            account['transactions'] = []
            for line in file_in:
                comment, amount = line.strip().split(':')
                account['transactions'].append({'comment': comment, 'amount': float(amount)})
        print("Данные аккаунта загружены.")
    except FileNotFoundError:
        print("Файл данных не найден. Создайте новый аккаунт.")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")

def main():
    print("Загрузить ваши данные?" + "\n" + "1. Да" + "\n" + "2. Нет")
    choice = int(input("Выберите вариант: "))
    if choice == 1:
        load_from_file()
        load_password_hash()
    elif choice == 2:
        print("Начните с создания нового аккаунта.")

    while True:
        print("\nДоступные операции:")
        print("1. Создать аккаунт")
        print("2. Положить деньги на счёт")
        print("3. Снять деньги со счёта")
        print("4. Вывести баланс на экран")
        print("5. Создать транзакцию")
        print("6. Установить лимит")
        print("7. Применить транзакции")
        print("8. Статистика транзакций")
        print("9. Фильтр транзакций по сумме")
        print("10. Выйти из программы")

        try:
            cmd = int(input("Выберите номер операции: "))
            if cmd == 1:
                create_account()
            elif cmd == 2:
                deposit_money()
            elif cmd == 3:
                withdraw_money()
            elif cmd == 4:
                print("Ваш текущий баланс: ", account['balance'])
            elif cmd == 5:
                handle_transaction()
            elif cmd == 6:
                set_threshold()
            elif cmd == 7:
                apply_transactions()
            elif cmd == 8:
                show_transaction_stats()
            elif cmd == 9:
                show_filtered_transactions()
            elif cmd == 10:
                print("Выход из программы...")
                break
            else:
                print("Неверный номер операции или аккаунт не создан.")
        except ValueError:
            print("Номер операции должен быть числом.")
        save_to_file()

if __name__ == "__main__":
    main()
