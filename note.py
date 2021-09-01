import json
import re
from address_book import load_note, dump_note

# Нужно прописать путь к NOTE_FILE с заметками
NOTE_FILE = 'note.json'

NOTE = load_note(NOTE_FILE)


def add_note():
    """Функция создания заметки"""
    result = 'Ваша заметка успешно сохранена.\n'
    new_note = input('Введите имя заметки: ')
    # Проверяем, есть ли заметка с таким заголовком в базе
    check_note_name(NOTE, new_note)
    new_note_tags = input('Введите один или несколько тегов заметки: ')
    # Сплитим все заметки в список
    tags = re.split(r'[ ,]+', new_note_tags)
    for tag in tags:
        tags[tags.index(tag)] = '#' + tag
    new_note_text = input('Ваша заметка: ')
    created_note = {'name': new_note, 'tag': tags, 'text': new_note_text}
    NOTE.append(created_note)
    for k, v in created_note.items():
        if not isinstance(v, list):
            result += f'{k.title()}: {v}\n'
        else:
            if len(v) != 1:
                result += f'{k.title()}: {", ".join(v)}\n'
            else:
                result += f'{k.title()}: {v[0]}\n'
    result += '\n'
    return result


def check_note_name(note_data, input_note_name):
    """Функция проверка существования заголовка в списке"""
    for note in note_data:
        if note['name'] == input_note_name:
            check1 = str(input(
                'Заметка с таким именем уже есть. Пожалуйста, уточните, вы хотите отредактировать заметку,'
                'или создать новую? edit_note/add_note: '))
            if check1 == 'edit_note':
                # Тут нужно будет вызывать ф-цию изменения заметки, передавая в нее input_note_name
                pass
            # Если юзер выбирает создать заметку - перезапускаем ф-цию add_note сначала
            elif check1 == 'add_note':
                add_note(NOTE_FILE)


def delete_note():
    """Функция удаления заметок по заголовку"""
    is_found = True
    note_title = str(input("Введите заголовок заметки для удаления.\n>>> "))
    for note in NOTE:
        if note_title == note['name']:
            is_found = False
            index = NOTE.index(note)
            NOTE.pop(index)
            return print(f"Заметка с заголовком: '{note_title}' успешно удалена.")
    if is_found:
        print(f"Заметка c заголовком: '{note_title}', отсутствует.")


def edit_note():
    """Функция редактирования заметки"""
    is_found = True
    note_name = str(input("Введите заголовок заметки для редактирования.\n>>>  "))
    for note in NOTE:
        if note_name == note['name']:
            is_found = False
            while True:
                value_to_change = input("What to edit? Text, tag or name. For exit N. :  ")
                if value_to_change.lower() == "n":
                    break
                elif value_to_change.lower() == 'text':
                    note_text = input("Enter text: ")
                    note['text'] = note_text
                elif value_to_change.lower() == 'name':
                    note_name = input("Enter name: ")
                    note['name'] = note_name
                elif value_to_change.lower() == 'tag':
                    note_tag = input("Enter tag: ")
                    tag_list = note['tag']
                    if note_tag in tag_list:
                        tag_list.remove(note_tag)
                    else:
                        tag_list.append(note_tag)
                else:
                    print("You have chosen the wrong command. Please repeat")

            print(f"Note {note_name} has been edited")
    if is_found:
        print(f"Note {note_name} not found")