import logging
import json
from clean import main
from address_book import *
from note import *
# from address_book import CONTACTS, add_contact, delete_contact, change_contact, search_contact, show_contacts



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
    path = input('Укажите папку для сортировки: ')
    main(path)
    return f'Сортировка окончена.'


def exit_handler():
    # print(CONTACTS)
    # print('Bye!')
    dump_note(ADDRESS_BOOK_FILE, CONTACTS)
    dump_note(NOTE_FILE, NOTE)
    return


@handle_info
def unknown_cmd():
    return "Unknown command."


COMMAND = {'add_contact': add_contact,
           'delete_contact': delete_contact,
           'change_contact': change_contact,
           'search_contact': search_contact,
           'show_contacts': show_contacts,
           'show_birthdays': show_birthdays,
           'add_note': add_note,
           'delete_note': delete_note,
           'change_note': '',
           'search_note': '',
           'show_notes': '',
           'sort_folder': sort_folder,
           'exit': exit_handler}


def main():
    print(f'Список команд: {[i for i in COMMAND.keys()]}')
    while True:
        user_input = input('Input your command: ')
        command = user_input.lower().strip()
        handler = COMMAND.get(command.lower(), unknown_cmd)
        result = handler()
        if not result:
            exit_handler()
            print('Bye')
            break
        print(result)


if __name__ == '__main__':
    main()