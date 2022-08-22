import databases.mongo_connect
from databases.mongo_models import Note, Record, Tag


def add_note():
    """Функция создания заметки"""
    name = input('Введите заголовок заметки для создания.\n>>> ')
    text = input('Введите текст заметки для создания.\n>>> ')
    tag = input('Введите теги заметки в формате: #Покупки #Развлечения.\n>>> ')
    note = Note(name=name, records=[Record(description=text), ], tags=[Tag(name=tag), ]).save()
    print(note.records)


def delete_note():
    """Функция удаления заметок по заголовку"""
    is_found = True
    note_title = str(input("Введите заголовок заметки для удаления.\n>>> "))

def change_note():
    """Функция редактирования заметки"""


def show_notes():
    """Функция вывода всех заметок"""
    notes = Note.objects()
    result = ''
    if notes:
        for note in notes:
            result = f'''
            Заголовок заметки: {note.name}
            Teкст заметки {[r.description for r in note.records]}
            Тег заметки {note.tags}\n
            '''
        return result
    else:
        result = 'К сожалению, нет ни единой заметки'
        return result


def find_note():
    """Функция поиска заметок по заголовку и тегу"""
    search_value = input('Пожалуйста, введите имя или тег заметки для поиска.\n>>> ')

