import sys

account = {'full_name': '', 'age': 0, 'login': '', 'password': '', 'password_hash': '',
           'balance': 0, 'threshold': 0, 'transactions': [], 'pending_payments': []}


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


def create_account(full_name, birth_year, login, password):
    try:
        account['full_name'] = full_name
        account['age'] = 2024 - birth_year
        account['login'] = login
        account['password'] = password
        account['password_hash'] = hash_password(password)
        save_password_hash()
        save_to_file()
        return f"Создан аккаунт: {account['full_name']} {account['age']} лет, Логин: {account['login']}"
    except ValueError:
        log_error("Неверный формат года рождения.")
    except Exception as e:
        log_error(e)


def deposit_money(login, amount):
    try:
        load_from_file(login)
        if amount > 0:
            account['balance'] += amount
            process_pending_payments()
        else:
            log_error("Сумма должна быть больше нуля.")
        save_to_file()
        return account['balance']
    except ValueError:
        log_error("Неверный формат суммы, должно быть число.")
    except Exception as e:
        log_error(f"Ошибка при пополнении счёта: {e}")


def withdraw_money(login, password, amount):
    try:
        load_from_file(login)
        if hash_password(password) == account['password_hash']:
            if amount > account['balance']:
                log_error("Недостаточно средств на счету.")
            elif amount <= 0:
                log_error("Сумма должна быть больше нуля.")
            else:
                account['balance'] -= amount
                save_to_file()
                return account['balance']
        else:
            log_error("Неверный пароль!")
    except ValueError:
        log_error("Ошибка при вводе суммы.")
    except Exception as e:
        log_error(f"Ошибка при снятии средств: {e}")


def handle_transaction(login, comment, amount):
    try:
        load_from_file(login)
        transaction = {'comment': comment, 'amount': amount}
        account['transactions'].append(transaction)
        save_to_file()
        return account['transactions']
    except ValueError:
        log_error("Ошибка при вводе данных транзакции.")
    except Exception as e:
        log_error(f"Ошибка при добавлении транзакции: {e}")


def set_threshold(login, threshold):
    try:
        load_from_file(login)
        account['threshold'] = threshold
        save_to_file()
        return account['threshold']
    except ValueError:
        log_error("Ошибка при установке лимита. Введите число.")
    except Exception as e:
        log_error(f"Ошибка при установке лимита: {e}")


def apply_transactions(login):
    try:
        load_from_file(login)
        new_transactions = []
        for transaction in account['transactions']:
            if transaction['amount'] <= account['threshold']:
                account['balance'] += transaction['amount']
            else:
                new_transactions.append(transaction)
        account['transactions'] = new_transactions
        save_to_file()
        return account['balance']
    except Exception as e:
        log_error(f"Ошибка при применении транзакций: {e}")


def show_transaction_stats(login):
    try:
        load_from_file(login)
        freq = {}
        for transaction in account['transactions']:
            amount = transaction['amount']
            if amount in freq:
                freq[amount] += 1
            else:
                freq[amount] = 1
        return freq
    except Exception as e:
        log_error(f"Ошибка при отображении статистики транзакций: {e}")


def filter_by_amount(login, filter_amount):
    try:
        load_from_file(login)
        filtered_transactions = [t for t in account['transactions'] if t['amount'] >= filter_amount]
        return filtered_transactions
    except ValueError:
        log_error("Неверный формат суммы, должно быть число.")
    except Exception as e:
        log_error(f"Ошибка при фильтрации транзакций: {e}")


def delayed_payment(sender_login, sender_password, recipient_login, amount):
    try:
        load_from_file(sender_login)

        if hash_password(sender_password) != account['password_hash']:
            log_error("Неверный пароль!")
            return

        if account['balance'] >= amount:
            account['balance'] -= amount
            save_to_file()

            recipient_data = load_account_data(recipient_login)
            recipient_data['balance'] += amount
            save_account_data(recipient_data)

            return "Платеж успешно выполнен."
        else:
            account['pending_payments'].append({'recipient_login': recipient_login, 'amount': amount})
            save_to_file()
            return "Недостаточно средств. Платеж сохранен для будущего исполнения."
    except ValueError:
        log_error("Неверный формат суммы, должно быть число.")
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
        account = {'full_name': '', 'age': 0, 'login': '', 'password': '', 'password_hash': '', 'balance': 0,
                   'threshold': 0, 'transactions': [], 'pending_payments': []}
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
                full_name = input("Введите Ф.И.О: ")
                birth_year = int(input("Введите год рождения: "))
                login = input("Введите логин: ")
                password = input("Введите пароль: ")
                print(create_account(full_name, birth_year, login, password))
            elif cmd == 2:
                login = input("Введите логин: ")
                amount = float(input("Введите сумму пополнения: "))
                print("Ваш текущий баланс: ", deposit_money(login, amount))
            elif cmd == 3:
                login = input("Введите логин: ")
                password = input("Введите пароль: ")
                amount = float(input("Введите сумму для снятия: "))
                print("Ваш текущий баланс: ", withdraw_money(login, password, amount))
            elif cmd == 4:
                login = input("Введите логин: ")
                load_from_file(login)
                print("Ваш текущий баланс: ", account['balance'])
            elif cmd == 5:
                login = input("Введите логин: ")
                comment = input("Введите комментарий для транзакции: ")
                amount = float(input("Введите сумму: "))
                print(handle_transaction(login, comment, amount))
            elif cmd == 6:
                login = input("Введите логин: ")
                threshold = float(input("Введите новый лимит транзакций: "))
                print("Ваш новый лимит: ", set_threshold(login, threshold))
            elif cmd == 7:
                login = input("Введите логин: ")
                print("Ваш текущий баланс: ", apply_transactions(login))
            elif cmd == 8:
                login = input("Введите логин: ")
                print("Статистика транзакций: ", show_transaction_stats(login))
            elif cmd == 9:
                login = input("Введите логин: ")
                filter_amount = float(input("Введите сумму для фильтрации: "))
                print("Фильтр транзакций: ", filter_by_amount(login, filter_amount))
            elif cmd == 10:
                sender_login = input("Введите логин отправителя: ")
                sender_password = input("Введите пароль отправителя: ")
                recipient_login = input("Введите логин получателя: ")
                amount = float(input("Введите сумму платежа: "))
                print(delayed_payment(sender_login, sender_password, recipient_login, amount))
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
