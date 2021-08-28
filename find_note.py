import json


# file_name - файл с заметками

def find_note(file_name):
    value = input('Пожалуйста, введите запрос имя или тег заметки: ')
    # Дессереализуем файл json
    with open(file_name, 'r') as f:
            decoded_data = json.load(f)
    # Счетчик для определения, найден результат запроса, или нет
    cnt = 0
    # Проверяем, поиск ведется по тегу или по имени
    if value.find('#') == 0:
        for note in decoded_data:
            if value in note['tag']:
                # упаковываем теги в строку для читабельного отображения
                tags = ', '.join(note['tag'])
                print(f"Заметка: {note['name']}\nТеги: {tags}\nТекст: {note['text']}\n================")
                cnt +=1
        if cnt == 0:
            print(f'Заметка по тегу {value} не найдена.')
    else:
        for note in decoded_data:
            if value == note['name']:
                tags = ', '.join(note['tag'])
                print(f"Заметка: {note['name']}\nТеги: {tags}\nТекст: {note['text']}\n================")
                cnt +=1
        if cnt == 0:
            print(f'Заметка по имени {value} не найдена.')




