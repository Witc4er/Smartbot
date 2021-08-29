import json
import re


#Нужно прописать путь к file_name с заметками
file_name = 'test.json'


def add_note(file_name):
    #Сохраняем инфу из файла в переменную decoded_data. Если файла нет - создаем список decoded_data, который в последствии сериализуем в json.
    try:
        with open(file_name, 'r') as fh:
            decoded_data = json.load(fh)
    except json.decoder.JSONDecodeError:
        decoded_data = []
    new_note = input('Введите имя заметки: ')
    #Проверяем, есть ли заметка с таким заголовком в базе
    check_note_name(decoded_data, new_note)
    new_note_tags = input('Введите один или несколько тегов заметки: ')
    #Сплитим все заметки в список
    tags = re.split(r'[ ,]+', new_note_tags)
    for tag in tags:
        tags[tags.index(tag)] = '#'+tag
    new_note_text = input('Ваша заметка: ')
    created_note = {'name': new_note, 'tag': tags, 'text': new_note_text}
    decoded_data.append(created_note)
    #Переписываем файл с заметками с учетом изменений
    with open(file_name, 'w') as fw:
        json.dump(decoded_data, fw)


def check_note_name(note_data, input_note_name):
    for note in note_data:
        if note['name'] == input_note_name:
            check1 = input('Заметка с таким именем уже есть. Пожалуйста, уточните, вы хотите отредактировать заметку, или создать новую? edit_note/add_note: ')
            if check1 == 'edit_note':
                #Тут нужно будет вызывать ф-цию изменения заметки, передавая в нее input_note_name
                pass
            #Если юзер выбирает создать заметку - перезапускаем ф-цию add_note сначала
            elif check1 == 'add_note':
                add_note(file_name)

add_note(file_name)
