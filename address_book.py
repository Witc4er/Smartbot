# ФУНКЦИИ ДЛЯ ОБРАБОТКИ ТЕЛЕФОНА
import re
import json
import os
from datetime import datetime, date

FILE_NAME = 'test.json'


def dump_note(new_data):
    with open(FILE_NAME, 'w') as fh:
        json.dump(new_data, fh)


def load_note(path_file):
    try:
        with open(path_file, 'r') as fh:
            return json.load(fh)
    except FileNotFoundError:
        return list()
    except Exception:
        return list()


CONTACTS = load_note(FILE_NAME)


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
    phone = input("Введите телефон: ")
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
                   "Что бы пропустить - нажмите 'Enter'.\n>>> ")
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


def add_contact():
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
           f'Номер телефона: {",".join(result["phones"])}\n' \
           f'Email: {result["email"]}\n'


def delete_contact():
    contact_name = input("Введите имя контакта для удаления: ")
    for contact in CONTACTS:
        if contact_name == contact['name']:
            CONTACTS.pop(CONTACTS.index(contact))
            return f"Контакт с именем: {contact_name}, успешно удален"
        return f'Контакт с именем: {contact_name}, в списке не найден'


def show_contacts():
    result = ''
    for contact in CONTACTS:
        for k, v in contact.items():
            result += f'{v}\n'
        result += '\n'
    return result


def is_exist_name_contact(contact_name):
    try:
        is_found = True

        if os.stat(FILE_NAME).st_size == 0:  # Проверяем пустой список или нет
            return print('empty')
        load_data = load_note(FILE_NAME)

        for contact in load_data:
            if contact_name == contact['name']:
                is_found = False
                check1 = input(
                    "Contact's name is exist. Are you editing or creating a contact? edit_contact/add_contact: ")
                if check1 == 'edit_contact':
                    # edit_contact()
                    print("Contact has been edited")
                elif check1 == 'add_contact':
                    # edit_contact()
                    print("Contact has been added")

        if is_found:
            print(f"Contact {contact_name} not found")

    except FileNotFoundError:
        print("File not found")


def show_birthday():
    cnt = 0
    result = ''
    current_date = date.today()
    # Парсим список по записям
    try:
        for contact in CONTACTS:
        # Формируем новую дату др с актуальным годом
            new_bd_day = datetime.strptime(contact['birthday'], '%d.%m.%Y').day
            new_bd_month = datetime.strptime(contact['birthday'], '%d.%m.%Y').month
            new_bd = date(year=current_date.year, month=new_bd_month, day=new_bd_day)
            # считаем дельту между др и сегодня
            delta = new_bd - current_date
            # если дельта меньше 7 - отображаем в консоль имя: дата
            if delta.days < 7:
                result += f"{contact['name']}: {contact['birthday']}\n\n"
                return result
                cnt += 1
        if cnt == 0:
            print('В ближайшие 7 дней именинников нет.')
    except KeyError:
        print('В записной книге пока ещё нет контактов с указанными датами рождения.')