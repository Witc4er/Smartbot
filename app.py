COMMAND = ['add_contact', 'delete_contact', 'change_contact', 'search_contact', 'show_contacts', 'show_birthday',
           'add_note', 'delete_note', 'change_note', 'search_note', 'show_notes']


def main():
    while True:
        user_input = input('Input your command: ')
        command = user_input.lower()
        if command in COMMAND:
            handler = COMMAND.get(command.lower(), 'unknown_cmd')


if __name__ == '__main__':
    main()