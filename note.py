import json
import re
from address_book import load_note
from pathlib import Path

# Путь к файлу с заметками
FILES = Path() / 'files'
FILES.mkdir(exist_ok=True)
NOTE_FILE = 'files/note.json'
# Заметки
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
            if check1 == 'change_note':
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


def change_note():
    """Функция редактирования заметки"""
    is_found = True
    note_name = str(input("Введите заголовок заметки для редактирования.\n>>>  "))
    for note in NOTE:
        if note_name == note['name']:
            is_found = False
            while True:
                value_to_change = str(input("Введите имя поля, которое хотите отредактировать:"
                                            " 'name', 'text' либо 'tag'.\n"
                                            "Чтобы выйти - просто нажмите 'Enter'.\n>>> ").strip())
                if value_to_change.lower() == "":
                    break
                elif value_to_change.lower() == 'text':
                    note_text = str(input("Enter text.\n>>> "))
                    note['text'] = note_text
                elif value_to_change.lower() == 'name':
                    note_name = str(input("Enter name.\n>>> "))
                    note['name'] = note_name
                elif value_to_change.lower() == 'tag':
                    note_tag = str(input("Enter tag.\n>>> "))
                    tag_list = note['tag']
                    if note_tag in tag_list:
                        tag_list.remove(note_tag)
                    else:
                        tag_list.append(note_tag)
                else:
                    return "Вы ввели неверную команду, пожалуйста, попробуйте еще раз."
            return f"Заметка успешно изменена."
    if is_found:
        return f"Заметка с заголовком: '{note_name}', отсутствует."


def show_notes() -> str:
    """Функция вывода всех заметок"""
    result = ''
    if NOTE:
        for note in NOTE:
            for k, v in note.items():
                if not isinstance(v, list):
                    result += f'{k.title()}: {v}\n'
                else:
                    if len(v) != 1:
                        result += f'{k.title()}: {", ".join(v)}\n'
                    else:
                        result += f'{k.title()}: {v[0]}\n'
            result += '\n'
        return result
    else:
        result = 'Нет записей в заметках.'
        return result


def find_note():
    """Функция поиска заметок по заголовку и тегу"""
    search_value = input('Пожалуйста, введите имя или тег заметки для поиска.\n>>> ')
    # Счетчик для определения, найден результат запроса, или нет
    cnt = 0
    # Проверяем, поиск ведется по тегу или по имени
    if search_value.find('#') == 0:
        for note in NOTE:
            if search_value in note['tag']:
                # упаковываем теги в строку для читабельного отображения
                tags = ', '.join(note['tag'])
                return f"Заметка: {note['name']}\nТеги: {tags}\nТекст: {note['text']}\n"
                cnt += 1
        if cnt == 0:
            return f'Заметка по тегу {search_value} не найдена.'
    else:
        for note in NOTE:
            if search_value == note['name']:
                tags = ', '.join(note['tag'])
                return f"Заметка: {note['name']}\nТеги: {tags}\nТекст: {note['text']}\n"
                cnt += 1
        if cnt == 0:
            return f'Заметка c именем: {search_value}, не найдена.'