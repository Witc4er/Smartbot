# ФУНКЦИИ ДЛЯ ОБРАБОТКИ ТЕЛЕФОНА
import re
from datetime import datetime, timedelta
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from databases.sql_models import AddressBook


engine = create_engine('sqlite:///smartbot.db')
Session = sessionmaker(bind=engine)
session = Session()


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
    return ';'.join(phones_to_add)


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
        check_email = is_email_correct(answer)
        if check_email:
            return check_email
        else:
            print("Вы ввели недействительный email.\nПопробуйте еще раз.")
            return wanna_enter_email()


def add_some_emails():
    list_emails = []
    first_mail = wanna_enter_email()
    if first_mail:
        list_emails.append(first_mail)
    while True:
        answer = input("Если хотите добавит еще один номер - введите его.\n"
                       "Если хотите продолжить - нажмите 'Enter'.\n>>> ")
        if answer == "":
            break
        else:
            check_email = is_email_correct(answer)
            if check_email:
                list_emails.append(check_email)
            else:
                print("Вы ввели недействительный email.\nПопробуйте еще раз.")
                return wanna_enter_email()
    return ';'.join(list_emails)


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
    result["email"] = add_some_emails()
    data_to_insert = AddressBook(
        name=result["name"],
        birthday=datetime.strptime(result["birthday"], '%d.%m.%Y'),
        address=result["address"],
        phone=result["phones"],
        email=result["email"]
    )
    session.add(data_to_insert)
    session.commit()
    return f'В записную книжку добавлена запись.\n' \
           f'Имя: {result["name"]}\n' \
           f'Дата рождения: {result["birthday"]}\n' \
           f'Адрес проживания: {result["address"]}\n' \
           f'Номер телефона: {result["phones"]}\n' \
           f'Email: {result["email"]}\n'


def delete_contact() -> str:
    # Функция удаления контакта
    contact_name = input("Введите имя контакта для удаления: ")
    try:
        i = session.query(AddressBook).filter(AddressBook.name == contact_name).one()
        session.delete(i)
        session.commit()
        return f"Контакт с именем: {contact_name}, успешно удален."
    except NoResultFound:
        return f'Контакт с именем: {contact_name}, в базе не найден.'


def show_contacts() -> str:
    # Функция вывода всех контактов
    contacts = session.query(AddressBook).all()
    if contacts:
        for i in contacts:
            print(i)
        return '----' * 10
    else:
        result = 'Нет записанных контактов.'
        return result


def find_contact():
    """Функция поиска контакта по имени"""
    name_for_search = input("Введите имя.\n>>> ")
    try:
        contact = session.query(AddressBook).filter(AddressBook.name == name_for_search).one()
        return contact
    except NoResultFound:
        return f'Контакт с именем: {name_for_search}, в базе не найден.'



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
    name_for_search = str(input("Введите имя.\n>>> ")).strip()
    try:
        contact = session.query(AddressBook).filter(AddressBook.name == name_for_search).one()
        print(contact)
        i_wanna_change = input("\nВведите цифру поля, которое хотите отредактировать и нажмите 'Enter'.\n"
                               "Чтобы выйти - просто нажмите 'Enter'.\n>>> ")
        if i_wanna_change == "1":
            i_wanna_change = input("\nПоле 'Id' невозможно отредактировать.\n"
                                   "Введите цифру поля, которое хотите отредактировать и нажмите 'Enter'.\n"
                                   "Чтобы выйти - просто нажмите 'Enter'.\n>>> ")
        if i_wanna_change == "2":
            contact.name = input("Введите новое имя контакта.\n>>> ")
        elif i_wanna_change == "3":
            contact.birthday = wanna_enter_birthday()
        elif i_wanna_change == "4":
            contact.address = str(input("Введите новый адресс контакта.\n>>> "))
        elif i_wanna_change == "5":
            contact.email = add_some_emails()
        elif i_wanna_change == "6":
            contact.phone = add_some_phones()

        else:
            return "Вы завершили редактирование контакта. Никаких изменений не произошло."
        session.add(contact)
        session.commit()
        return f'Изменения успешно сохранены.'
    except NoResultFound:
        return f'Контакта с именем: {name_for_search}, в базе нет.'
