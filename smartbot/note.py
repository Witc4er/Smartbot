import databases.mongo_connect
from databases.mongo_models import Note, Record, Tag

import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host='localhost', port=6379, password=None)
cache = RedisLRU(client)



def add_note():
    """Функция создания заметки"""
    name = input('Введите заголовок заметки для создания.\n>>> ')
    text = input('Введите текст заметки для создания.\n>>> ')
    tag = input('Введите теги заметки в формате: #Покупки #Развлечения.\n>>> ')
    note = Note(name=name, records=[Record(description=text), ], tags=[Tag(name=tag), ]).save()
    print(note.records)


def delete_note():
    """Функция удаления заметок по заголовку"""
    note_title = str(input("Введите заголовок заметки для удаления.\n>>> "))
    note = Note.objects(name=note_title).first()
    result = f'Заметка с заголовком "{note_title}" успешно удалена.'
    if note:
        result += prepare_note(note)
        note.delete()
        return result
    else:
        result = 'Заметка с указанным заголовком отсутствует в базе.'
        return result


def change_note():
    """Функция редактирования заметки"""
    name = input('Введите заголовок заметки для изменения.\n>>> ')
    note = Note.objects(name=name).first()
    result = ''
    if note:
        result = prepare_note(note)
        print(result)
        change_item = int(input('Введите номер поля для редактирования.\n>>> '))
        if change_item == 1:
            note.update(name=input('Введите новый заголовок заметки. \n>>> '))
        elif change_item == 2:
            new_text = input('Введите новый текст заметки. \n>>> ')
            note.update(records=[Record(description=new_text), ])
        elif change_item == 3:
            new_tag = input('Введите новый текст заметки. \n>>> ')
            note.update(tags=[Tag(name=new_tag, )])
        print('Информация успешно обновлена.')

    else:
        result = 'Заметка с указанным заголовком отсутствует в базе.'
        return result


def prepare_note(note):
    result = f'\n1. Заголовок заметки: {note.name}\n' \
            f'2. Teкст заметки: {",".join([r.description for r in note.records])}\n' \
            f'3. Тег заметки: {",".join([t.name for t in note.tags])}\n'
    return result

@cache
def show_notes():
    print('Call function show notes')
    """Функция вывода всех заметок"""
    notes = Note.objects()
    result = ''
    if notes:
        for note in notes:
            result += prepare_note(note)
        return result
    else:
        result = 'К сожалению, нет ни единой заметки'
        return result
@cache
def find_note():
    """Функция поиска заметок по заголовку и тегу"""
    search_value = input('Пожалуйста, введите имя заметки для поиска.\n>>> ')
    notes = Note.objects(name=search_value)
    result = ''
    if notes:
        for note in notes:
            result += prepare_note(note)
        return result
    else:
        result = 'К сожалению, нет заметок с указанным именем.'
        return result


