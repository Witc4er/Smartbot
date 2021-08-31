import logging
import json
from clean import main
from address_book import add_contact, delete_contact, CONTACTS, dump_note, show_contacts, show_birthday


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
    print(CONTACTS)
    dump_note(CONTACTS)
    return


@handle_info
def unknown_cmd():
    return "Unknown command"


COMMAND = {'add_contact': add_contact,
           'delete_contact': delete_contact,
           'change_contact': '',
           'search_contact': '',
           'show_contacts': show_contacts,
           'show_birthday': show_birthday,
           'add_note': '',
           'delete_note': '',
           'change_note': '',
           'search_note': '',
           'show_notes': '',
           'sort_folder': sort_folder,
           'exit': exit_handler}


def main():
    print(f'Список команд: {[i for i in COMMAND.keys()]}')
    while True:
        user_input = input('Input your command: ')
        command = user_input.lower()
        handler = COMMAND.get(command.lower(), unknown_cmd)
        result = handler()
        if not result:
            print('Bye!')
            break
        print(result)


if __name__ == '__main__':
    main()