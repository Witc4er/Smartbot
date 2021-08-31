from fuzzywuzzy import fuzz


def command_analyzer():
    input_command = input("Введите команду: ")
    main_commands = [
                     "add_contact", "delete_contact", "change_contact", "search_contact", "show_contacts", 
                     "show_birthday", "add_note", "delete_note", "change_note", "search_note", "show_notes"
                    ]
    
    for command in main_commands:
        if 70 < fuzz.ratio(command, input_command) < 100:
            print(f"Похоже, вы имели ввиду {command}")
            return command
        elif fuzz.ratio(command, input_command) == 100:
            return command

    print("Простите, команда не распознана. Повторите попытку.")
    command_analyzer()

command_analyzer()

#Функция сама просит ввести команду, а return отдает ту у которой болший процент совпадения.
#Для работы нужно pip install fuzzywuzzy
#requirements.txt прилагается