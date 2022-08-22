import logging
from smartbot.sort_file import *
from smartbot.address_book import *
from smartbot.note import *
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
    """Функция выхода из бота"""
    return


def possible_cmd():
    """Функция вывода сообщения если неверно указана команда"""
    return f'К сожалению, команда не распознана. Вероятно, вы имели ввиду что-то из этого: {", ".join(psb_cmd)}\n' \
           f"Попробуйте ввести команду еще раз."


def unknown_cmd():
    """Функция вывода сообщения если введена неизвестная команда"""
    return f'К сожалению, команда не распознана.' \
           f"Попробуйте ввести команду еще раз."


COMMAND = {'add_contact': add_contact,
           'delete_contact': delete_contact,
           'change_contact': change_contact,
           'find_contact': find_contact,
           'show_contacts': show_contacts,
           'add_note': add_note,
           'delete_note': delete_note,
           'change_note': change_note,
           'find_note': find_note,
           'show_notes': show_notes,
           'sort_folder': sort_folder,
           'exit': exit_handler}


# Список вероятных команд
psb_cmd = []

def command_analyzer(input_command):
    """Функция, которая занимается анализом введенных команд"""
    for key, value in COMMAND.items():
        if fuzz.ratio(key, input_command) == 100:
            return value
        elif 80 < fuzz.ratio(key, input_command) < 100:
            print(f"Похоже, вы имели ввиду команду: {key}")
            return value
        elif 40 <= fuzz.ratio(key, input_command) <= 80:
            psb_cmd.append(key)
    if len(psb_cmd) > 0:
        return possible_cmd
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