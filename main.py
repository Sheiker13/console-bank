import sys

account = {'full_name': '', 'age': 0, 'login': '', 'password': '', 'password_hash': '', 'balance': 0, 'threshold': 0, 'transactions': [], 'pending_payments': []}

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
        with open(f"{account['login']}.passwordhash.txt", "w") as file_out:
            file_out.write(account['password_hash'])
    except Exception as e:
        log_error(f"Ошибка при сохранении хеша пароля: {e}")

def load_password_hash(login):
    try:
        with open(f"{login}.passwordhash.txt", "r") as file_in:
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
        account['login'] = input("Введите логин: ")
        password = input("Введите пароль: ")
        account['password'] = password
        account['password_hash'] = hash_password(password)
        save_password_hash()
        save_to_file()
        print(f"Создан аккаунт: {account['full_name']} {account['age']} лет, Логин: {account['login']}")
        print("Аккаунт успешно зарегистрирован!")
    except Exception as e:
        log_error(e)

def deposit_money():
    try:
        login = input("Введите логин: ")
        load_from_file(login)
        amount = float(input("Введите сумму пополнения: "))
        if amount > 0:
            account['balance'] += amount
            print("Счёт успешно пополнен на сумму:", amount)
            process_pending_payments()
        else:
            print("Сумма должна быть больше нуля.")
        save_to_file()
    except ValueError:
        log_error("Неверный формат суммы, должно быть число.")
    except Exception as e:
        log_error(f"Ошибка при пополнении счёта: {e}")

def withdraw_money():
    try:
        login = input("Введите логин: ")
        load_from_file(login)
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
        save_to_file()
    except ValueError:
        log_error("Ошибка при вводе суммы.")
    except Exception as e:
        log_error(f"Ошибка при снятии средств: {e}")

def handle_transaction():
    try:
        login = input("Введите логин: ")
        load_from_file(login)
        comment = input("Введите комментарий для транзакции: ")
        amount = float(input("Введите сумму: "))
        transaction = {'comment': comment, 'amount': amount}
        account['transactions'].append(transaction)
        print(f"Транзакция добавлена. Комментарий: {comment}, сумма: {amount}")
        save_to_file()
    except ValueError:
        log_error("Ошибка при вводе данных транзакции.")
    except Exception as e:
        log_error(f"Ошибка при добавлении транзакции: {e}")

def set_threshold():
    try:
        login = input("Введите логин: ")
        load_from_file(login)
        threshold = float(input("Введите новый лимит транзакций: "))
        account['threshold'] = threshold
        print(f"Лимит транзакций установлен на: {threshold}")
        save_to_file()
    except ValueError:
        log_error("Ошибка при установке лимита. Введите число.")
    except Exception as e:
        log_error(f"Ошибка при установке лимита: {e}")

def apply_transactions():
    try:
        login = input("Введите логин: ")
        load_from_file(login)
        new_transactions = []
        for transaction in account['transactions']:
            if transaction['amount'] <= account['threshold']:
                account['balance'] += transaction['amount']
                print(f"Транзакция на {transaction['amount']} применена.")
            else:
                new_transactions.append(transaction)
                print(f"Транзакция на {transaction['amount']} отклонена из-за лимита.")
        account['transactions'] = new_transactions
        save_to_file()
    except Exception as e:
        log_error(f"Ошибка при применении транзакций: {e}")

def show_transaction_stats():
    try:
        login = input("Введите логин: ")
        load_from_file(login)
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
        login = input("Введите логин: ")
        load_from_file(login)
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

def delayed_payment():
    try:
        sender_login = input("Введите логин отправителя: ")
        sender_password = input("Введите пароль отправителя: ")
        recipient_login = input("Введите логин получателя: ")
        amount = float(input("Введите сумму платежа: "))

        load_from_file(sender_login)

        if hash_password(sender_password) != account['password_hash']:
            print("Неверный пароль!")
            return

        if account['balance'] >= amount:
            account['balance'] -= amount
            save_to_file()

            recipient_data = load_account_data(recipient_login)
            recipient_data['balance'] += amount
            save_account_data(recipient_data)

            print("Платеж успешно выполнен.")
        else:
            account['pending_payments'].append({'recipient_login': recipient_login, 'amount': amount})
            print("Недостаточно средств. Платеж сохранен для будущего исполнения.")
        save_to_file()
    except Exception as e:
        log_error(f"Ошибка при выполнении отложенного платежа: {e}")

def process_pending_payments():
    try:
        updated_payments = []
        for payment in account['pending_payments']:
            recipient_login = payment['recipient_login']
            amount = payment['amount']
            if account['balance'] >= amount:
                account['balance'] -= amount

                recipient_data = load_account_data(recipient_login)
                recipient_data['balance'] += amount
                save_account_data(recipient_data)

                print(f"Отложенный платеж на сумму {amount} для {recipient_login} выполнен.")
            else:
                updated_payments.append(payment)
        account['pending_payments'] = updated_payments
    except Exception as e:
        log_error(f"Ошибка при обработке отложенных платежей: {e}")

def save_account_data(account):
    try:
        with open(f"{account['login']}.account_data.txt", "w") as file_out:
            file_out.write(f"{account['full_name']}\n")
            file_out.write(f"{account['age']}\n")
            file_out.write(f"{account['login']}\n")
            file_out.write(f"{account['password']}\n")
            file_out.write(f"{account['password_hash']}\n")
            file_out.write(f"{account['balance']}\n")
            file_out.write(f"{account['threshold']}\n")
            for transaction in account['transactions']:
                file_out.write(f"{transaction['comment']}:{transaction['amount']}\n")
            for payment in account['pending_payments']:
                file_out.write(f"pending:{payment['recipient_login']}:{payment['amount']}\n")
        print("Данные аккаунта сохранены.")
    except Exception as e:
        log_error(f"Ошибка при сохранении данных: {e}")

def load_account_data(login):
    try:
        account = {'full_name': '', 'age': 0, 'login': '', 'password': '', 'password_hash': '', 'balance': 0, 'threshold': 0, 'transactions': [], 'pending_payments': []}
        with open(f"{login}.account_data.txt", "r") as file_in:
            account['full_name'] = file_in.readline().strip()
            account['age'] = int(file_in.readline().strip())
            account['login'] = file_in.readline().strip()
            account['password'] = file_in.readline().strip()
            account['password_hash'] = file_in.readline().strip()
            account['balance'] = float(file_in.readline().strip())
            account['threshold'] = float(file_in.readline().strip())
            for line in file_in:
                if line.startswith("pending:"):
                    _, recipient_login, amount = line.strip().split(':')
                    account['pending_payments'].append({'recipient_login': recipient_login, 'amount': float(amount)})
                else:
                    comment, amount = line.strip().split(':')
                    account['transactions'].append({'comment': comment, 'amount': float(amount)})
        print("Данные аккаунта загружены.")
        return account
    except FileNotFoundError:
        log_error("Файл данных не найден. Создайте новый аккаунт.")
        return None
    except Exception as e:
        log_error(f"Ошибка при загрузке данных: {e}")
        return None

def save_to_file():
    save_account_data(account)

def load_from_file(login):
    global account
    account = load_account_data(login)

def main():
    print("Загрузить ваши данные из файла?" + "\n" + "1. Да" + "\n" + "2. Нет")
    choice = input("Выберите вариант: ")
    if choice == "1":
        login = input("Введите логин: ")
        load_from_file(login)
        load_password_hash(login)
    elif choice == "2":
        print("Начните с создания нового аккаунта.")
    else:
        print("Неверный выбор. Начните с создания нового аккаунта.")

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
        print("10. Отложенный платеж")
        print("11. Выйти из программы")

        try:
            cmd = int(input("Выберите номер операции: "))
            if cmd == 1:
                create_account()
            elif cmd == 2:
                deposit_money()
            elif cmd == 3:
                withdraw_money()
            elif cmd == 4:
                login = input("Введите логин: ")
                load_from_file(login)
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
                delayed_payment()
            elif cmd == 11:
                print("Выход из программы...")
                break
            else:
                print("Неверный номер операции или аккаунт не создан.")
        except ValueError:
            log_error("Номер операции должен быть числом.")
        except Exception as e:
            log_error(f"Ошибка в главном цикле: {e}")

if __name__ == "__main__":
    main()
