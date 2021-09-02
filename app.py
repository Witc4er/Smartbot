import logging
import json
from clean import *
from address_book import *
from note import *
from fuzzywuzzy import fuzz



# Config logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG, datefmt='%d.%m.%Y %H:%M:%S')

# Init logger
logger = logging.getLogger()


def handle_info(func):
    def inner(*args):
        result = func(*args)
        logger.info(result)
        return result
    return inner


def sort_folder():
    path = input('Введите путь для сортировки.\n>>> ')
    try:
        result = sort_folder(path)
        return 'Сортировка окончена'
    except TypeError:
        return f'Вы не передали путь при вызове скрипта. Попробуйте еще раз.'


def exit_handler():
    # print(CONTACTS)
    # print('Bye!')
    dump_note(ADDRESS_BOOK_FILE, CONTACTS)
    dump_note(NOTE_FILE, NOTE)
    return


@handle_info
def unknown_cmd():
    return f"Простите, команда не распознана.\nПовторите попытку."


COMMAND = {'add_contact': add_contact,
           'delete_contact': delete_contact,
           'change_contact': change_contact,
           'search_contact': search_contact,
           'show_contacts': show_contacts,
           'show_birthdays': show_birthdays,
           'add_note': add_note,
           'delete_note': delete_note,
           'change_note': change_note,
           'search_note': search_note,
           'show_notes': show_notes,
           'sort_folder': sort_folder,
           'exit': exit_handler}


def command_analyzer(input_command):
    """Функция, которая занимается анализом введенных команд"""
    possible_cmd = []
    for key, value in COMMAND.items():
        if fuzz.ratio(key, input_command) == 100:
            return value
        elif 72 < fuzz.ratio(key, input_command) < 100:
            print(f"Похоже, вы имели ввиду команду: {key}")
            return value
        elif 40 <= fuzz.ratio(key, input_command) <= 70:
            possible_cmd.append(key)

    if len(possible_cmd) > 0:
        pos_cmd = ", ".join(possible_cmd)
        return f"К сожалению, команда не распознана. Вероятно, вы имели ввиду что-то из этого: {pos_cmd}\n" \
               f"Попробуйте ввести команду еще раз."
    else:
        return unknown_cmd


def main():
    print(f'Список команд: {[i for i in COMMAND.keys()]}')
    while True:
        user_input = input('Input your command: ')
        command = user_input.lower().strip()
        handler = command_analyzer(command)
        result = handler()
        if not result:
            exit_handler()
            print('Bye')
            break
        print(result)


if __name__ == '__main__':
    main()