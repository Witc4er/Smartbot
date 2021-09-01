from fuzzywuzzy import fuzz
from app import COMMAND

def command_analyzer():
    while True:
        input_command = input("Введите команду: ")
        possible_cmd = []
        for key, value in COMMAND.items():
            if 70 < fuzz.ratio(key, input_command) < 100:
                print(f"Похоже, вы имели ввиду {value}")
                return value
            elif fuzz.ratio(key, input_command) == 100:
                return value
            elif 40 <= fuzz.ratio(key, input_command) <= 70:
                possible_cmd.append(key)

        if len(possible_cmd) > 0:   
            pos_cmd = ", ".join(possible_cmd)
            print(f"К сожалению, команда не распознана. Вероятно, вы имели ввиду что-то из этого: {pos_cmd}")
        else:
            print(f"Простите, команда {input_command} - не распознана. Повторите попытку")

command_analyzer()

#Функция сама просит ввести команду, а return отдает ту у которой болший процент совпадения.
#Для работы нужно pip install fuzzywuzzy
#requirements.txt прилагается