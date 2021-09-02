# ФУНКЦИИ ДЛЯ ОБРАБОТКИ ТЕЛЕФОНА
import re
import json
import os
from datetime import datetime, date, timedelta

# Пусть к файлу с контактами
ADDRESS_BOOK_FILE = 'files/address_book.json'


def dump_note(path_file, new_data):
    """Функция записи данных в файл"""
    with open(path_file, 'w') as fh:
        json.dump(new_data, fh)


def load_note(path_file):
    """Функция чтения данных из файла"""
    try:
        with open(path_file, 'r') as fh:
            return json.load(fh)
    except FileNotFoundError:
        return list()
    except Exception:
        return list()

# Пусть к файлу с контактами
CONTACTS = load_note(ADDRESS_BOOK_FILE)


def sanitize_n_check_phone(phone):
    # Функция принимает на вход телефон с кодом страны или без, удаляет из него лишние символы, проверяет на валидность.
    # Если валиден - возвращает телефон в формате +380*********, иначе возвращает False
    def sanitize_phone_number(phone):
        # Убирает типичные лишние символы
        new_phone = (
            phone.strip()
                .removeprefix("+")
                .replace("(", "")
                .replace(")", "")
                .replace("-", "")
                .replace(" ", "")
        )
        return new_phone

    def check_phone_number(new_phone):
        # Функция проверяет валидность "нормализированного" номера и возвращает его в стандарте +380, или возвращает
        # False если невалиден
        sanitized_phone = sanitize_phone_number(phone)
        for symbol in sanitized_phone:  # должен содержать только цифры
            if symbol not in "0123456789":
                return False
        if sanitized_phone[0:3] == "380" and len(sanitized_phone) == 12:
            return "+" + str(sanitized_phone)  # наинаеться с 380 и имеет длинну 12
        elif sanitized_phone[0:1] == "0" and len(sanitized_phone) == 10:
            return "+38" + str(sanitized_phone)  # начинаться с 0 и имеет длинну 10
        else:
            return False

    return check_phone_number(sanitize_phone_number(phone))


def input_phone():
    # Дает возможность ввести телефон и проверяет его валидность.
    # Если невалиден - ввод еще раз, Если валиден - возвращает валидный телефон
    phone = input("Введите телефон.\n>>> ")
    if not sanitize_n_check_phone(phone):
        print("Вы ввели некоректный телефон.\nПопробуйте еще раз ;)")
        return input_phone()
    else:
        return sanitize_n_check_phone(phone)


def add_some_phones():
    # Возвращает список от одного и более валидных телефонов.
    # После коректного введения 1 телефона спросит, хочешь ли добавить еще.
    # И, если ты уже ввел хотя бы 1 валидный номер, а потом захотел ввести еще, но ввел неправильно или передумал
    # вводить, будет предложено не вводить телефон и двинутся дальше вместо " Ты ввел неправильно, попробуй еще"
    phones_to_add = list()
    phones_to_add.append(input_phone())
    while True:
        answer = input("Если хотите добавит еще один номер - введите его.\n"
                       "Если хотите продолжить - нажмите 'Enter'.\n>>> ")
        if answer == "":
            break
        else:
            if sanitize_n_check_phone(answer):
                phones_to_add.append(sanitize_n_check_phone(answer))
            else:
                print("Вы ввели невалидный телефон.\nПопробуйте еще раз.")
    return phones_to_add


def wanna_enter_address():
    # Функция обработки адресса
    # Просто дает возможность вводить или не вводить адресс. Проверки нет.

    answer = input("Введите адрес контакта и нажмите 'Enter'.\n"
                   "Что бы пропустить - нажмите 'Enter'.\n>>> ")
    if answer == "":
        return
    else:
        return answer


def is_email_correct(email):
    # ФУНКЦИИ ДЛЯ ОБРАБОТКИ ЭМЕЙЛА
    # 1. Дать возможность пропустить ввод емейла.
    # 2. Проверка введенного емейла ( )
    # Функция принимает введенный эмейл, проверяет его, если валиден - возвращает его, иначе - возвращает False

    check = re.match(r"[a-zA-Z._]{1}[a-zA-Z._0-9]+@[a-zA-Z]+\.[a-z]{2}[a-z]*", email)
    if check:
        return email
    return False
    # Критерии проверки:
    # 1. Все буквы только англ алфавита
    # 2. ПРЕФИКС (то что до @)
    # 2.1 начинаеться с латинской буквы, содержит любое число символов
    # 2.2 и может содержать любое число/букву включая нижнее подчеркивание
    # 3. СУФФИКС (то что после @)
    # 3.1 Состоит из двух частей, разделенных точкой
    # 3.2 После точки должно быть минимум 2 символа


def wanna_enter_email():
    # Функция ничего не принимает, возвращает либо валидное значение емейла, либо None
    # Функция дает возможность ввести эмейл или перейти дальше. В случае ошибки так же предложит пропустить или
    # попробовать заново.

    answer = input("Введите Email человека и нажмите 'Enter'.\n"
                   "Чтобы пропустить - нажмите 'Enter'.\n>>> ")
    if answer == "":
        return None
    else:
        if is_email_correct(answer):
            return is_email_correct(answer)
        else:
            print("Вы ввели недействительный email.\nПопробуйте еще раз.")
            return wanna_enter_email()


def is_date_correct(date):
    # ФУНКЦИИ ДЛЯ ОБРАБОТКИ ДАТЫ РОЖДЕНИЯ
    # 1. Дать возможность вводить или не вводить день рождения
    # 2. Проверка на соответствие заданному формату даты

    if re.match(r"(([0-2]{1}[0-9]{1})|([3]{1}[0-1])).(([0]{1}[0-9])|([1]{1}[0-2])).[0-9]{4}", date):
        return date
    # валидный формат даты: 01.12.1976
    return False


def wanna_enter_birthday():
    answer = input(
        "Введите день рождения человека в формате '01.09.1986' и нажмите 'Enter'.\n"
        "Чтобы пропустить - нажмите 'Enter'.\n>>> ")
    if answer == "":
        return None
    else:
        if is_date_correct(answer):
            return is_date_correct(answer)
        else:
            print("Вы ввели недействительную дату.\nПопробуйте еще раз.")
            return wanna_enter_birthday()


def add_contact() -> str:
    # Собранная функция добавления контакта
    # Не принимает аргументов, возвращает словарь с проверенными значениями имени, телефона (телефонов),
    # и по желанию - почта и день рождения
    result = dict()
    result["name"] = input("Введите имя контакта: ")
    result["birthday"] = wanna_enter_birthday()
    result["address"] = wanna_enter_address()
    result["phones"] = add_some_phones()
    result["email"] = wanna_enter_email()
    CONTACTS.append(result)
    return f'В записную книжку добавлена запись.\n' \
           f'Имя: {result["name"]}\n' \
           f'Дата рождения: {result["birthday"]}\n' \
           f'Адрес проживания: {result["address"]}\n' \
           f'Номер телефона: {", ".join(result["phones"])}\n' \
           f'Email: {result["email"]}\n'


def delete_contact() -> str:
    # Функция удаления контакта
    contact_name = input("Введите имя контакта для удаления: ")
    for contact in CONTACTS:
        if contact_name == contact['name']:
            CONTACTS.pop(CONTACTS.index(contact))
            return f"Контакт с именем: {contact_name}, успешно удален"
        return f'Контакт с именем: {contact_name}, в списке не найден'


def show_contacts() -> str:
    # Функция вывода всех контактов
    result = ''
    if CONTACTS:
        for contact in CONTACTS:
            for k, v in contact.items():
                if not isinstance(v, list):
                    result += f'{k.title()}: {v}\n'
                else:
                    if len(v) != 1:
                        result += f'{k.title()}: {", ".join(v)}\n'
                    else:
                        result += f'{k.title()}: {v[0]}\n'
            result += '\n'
        return result
    else:
        result = 'Нет записанных контактов.'
        return result


# def is_exist_name_contact(contact_name):
#     try:
#         is_found = True
#
#         if os.stat(ADDRESS_BOOK_FILE).st_size == 0:  # Проверяем пустой список или нет
#             return print('empty')
#         load_data = load_note(ADDRESS_BOOK_FILE)
#
#         for contact in load_data:
#             if contact_name == contact['name']:
#                 is_found = False
#                 check1 = input(
#                     "Contact's name is exist. Are you editing or creating a contact? edit_contact/add_contact: ")
#                 if check1 == 'edit_contact':
#                     # edit_contact()
#                     print("Contact has been edited")
#                 elif check1 == 'add_contact':
#                     # edit_contact()
#                     print("Contact has been added")

#     if is_found:
#         print(f"Contact {contact_name} not found")
#
# except FileNotFoundError:
#     print("File not found")


def close_birthday_users(users, start, end) -> list:
    # Функция выборки ближайших дней рождения
    now = datetime.today().date()
    result = []
    for user in users:
        try:
            birthday = datetime.strptime(user['birthday'], '%d.%m.%Y').date()
            birthday = birthday.replace(year=now.year)
        except TypeError:
            continue
        if start <= birthday <= end:
            result.append(user)
    return result


def show_birthdays(contacts=CONTACTS) -> str:
    # Функция выводы ближайших дней рождения контактов
    result = ''
    now = datetime.today().date()
    current_week_day = now.weekday()
    if current_week_day >= 5:
        start_date = now - timedelta(days=(7 - current_week_day))
    elif current_week_day == 0:
        start_date = now - timedelta(days=2)
    else:
        start_date = now
    days_ahead = 4 - current_week_day
    if days_ahead < 0:
        days_ahead += 7
    end_date = now + timedelta(days=days_ahead)
    birthday_users = close_birthday_users(contacts, start=start_date, end=end_date)
    for birthday in birthday_users:
        for k, v in birthday.items():
            if not isinstance(v, list):
                result += f'{k.title()}: {v}\n'
            else:
                if len(v) != 1:
                    result += f'{k.title()}: {", ".join(v)}\n'
                else:
                    result += f'{k.title()}: {v[0]}\n'
        result += '\n'
    if not result:
        return 'Ближайшие семь дней среди Ваших контактов именинников нет.'
    return result


def search_contact():
    """Функция поиска контакта по имени"""
    result = ''
    name_for_search = input("Введите имя.\n>>> ")
    for contact in CONTACTS:
        if contact["name"] == name_for_search:
            for k, v in contact.items():
                if not isinstance(v, list):
                    result += f'{v}\n'
                else:
                    if len(v) != 1:
                        result += f'{", ".join(v)}\n'
                    else:
                        result += f'{v[0]}\n'
            result += '\n'
            return result
    return


# # 2. Если запись не найдена - можно, ввести еще раз или отменить выполнение функции.
# def search_contact_cycle():
#     # Функциия принимает распакованный список контактов и возвращает искомый контакт (по ключу "name") или None, если человек выбрал прекратить поиск.
#     while True:
#         search_for_name = str(input("Введите имя контакта , чтобы прекратить нажмите только Enter: "))
#         pos_in_list = 0
#         if search_for_name == "":
#             return
#         for contact in CONTACTS:
#             if contact["name"] == search_for_name:
#                 return [contact]
#             pos_in_list += 1
#         print("Контакт с таким именем не найден.")


def wanna_change_smth_else():
    """Вложенная функция запроса на измениня каких-либо других полей"""
    answer = str(input("Изменения внесены. Если Хотите изменить что-то еще - введите любой символ и "
                       "нажмите 'Enter', чтобы выйти - просто нажмите 'Enter'.\n>>> "))
    if not answer:
        return 'ok'
    else:
        return change_contact()

# 3. Пользователю выводиться все поля контакта, и спрашиваеться, которое он хочет изменить.
# 4. Вызываеться функция изменения данного параметра
# 5. Спрашиваеться, нужно ли изменить что то еще
# 6. Если нужно изменить что то еще - начинаеться пунки 3.
def change_contact():
    """Функция изменения контакта"""
    # contact = search_contact()
    # Принимает на вход контакт, найденный функцией search_contact_cycle,
    # печатает поля контакта, и спрашивает, который нужно изменить.

    count = 0  # Эта часть кода отображает содержание контакта с нумерацией полей словаря
    name_for_search = str(input("Введите имя.\n>>> ")).strip()
    for contact in CONTACTS:
        # Проверка на предмет наличия контакта в списке контактов
        if contact["name"] == name_for_search:
            # Вывод перечня полей для контакта
            for key, value in contact.items():
                count += 1
                print(f"{count}. {key.title()}: {value}")
            #  Просьба ввести номер параметра, который нужно изменить, с последующим изменением
            i_wanna_change = input("\nВведите цифру поля, которое хотите отредактировать и нажмите 'Enter'.\n"
                                   "Чтобы выйти - просто нажмите 'Enter'.\n>>> ")
            if i_wanna_change == "1":
                contact["name"] = input("Введите новое имя контакта.\n>>> ")
            elif i_wanna_change == "2":
                contact["birthday"] = wanna_enter_birthday()
            elif i_wanna_change == "3":
                contact["address"] = str(input("Введите новый адресс контакта.\n>>> "))
            elif i_wanna_change == "4":
                def wanna_add_or_change_phone():
                    """Вложенная функция изменения телефона контакта"""
                    # Возвращает новый список телеофонов для этого контакта
                    # Отображение всех телефонов контакта с порядковым номером
                    count_phone = 0
                    for phones in contact["phones"]:
                        count_phone += 1
                        print(f"{count_phone}. {phones}")
                    answer = input(
                        "Если хотите добавить новый телефон - просто введите его,"
                        "если же хотите изменить существующий - введите его порядковый номер,"
                        "после чего укажите новый мобильный телефон.\n>>> ")
                    if len(answer) <= 2:  # проверка что ввел порядковый номер
                        contact["phones"][int(answer) - 1] = input_phone()  # Заменяет телефон в списке
                    else:
                        contact["phones"].append(input_phone)  # если ввел не порядковый номер, то предполагаем, телефо
                    return contact["phones"]

                contact["phones"] = wanna_add_or_change_phone()
            elif i_wanna_change == "5":
                contact["email"] = wanna_enter_email()
            elif i_wanna_change == "":
                return "Вы завершили редактирование контакта. Никаких изменений не произошло."
            return f'Изменения успешно сохранены'

        # return f'Контакт с именем: {name_for_search}, отсутствует в записной книжке.'
