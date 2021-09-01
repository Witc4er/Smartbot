from datetime import datetime, date
import json

file_name = 'test.json'



#На вход передаем наш файл json с контактами
def birthday_boys(file_name):
    cnt = 0
    try:
        with open('test.json', 'r') as f:
            contacts = json.load(f)
        current_date = date.today()
        #Парсим список по записям
        try:
            for contact in contacts:
            # формируем новую дату др с актуальным годом
                new_bd_day = datetime.strptime(contact['birthday'], '%d.%m.%Y').day
                new_bd_month = datetime.strptime(contact['birthday'], '%d.%m.%Y').month
                new_bd = date(year=current_date.year, month=new_bd_month, day=new_bd_day)
                #считаем дельту между др и сегодня
                delta = new_bd-current_date
                #если дельта меньше 7 - отображаем в консоль имя: дата
                if delta.days < 7:
                    print(f"{contact['name']}: {contact['birthday']}")
                    cnt+=1
            if cnt == 0:
                print('В ближайшие 7 дней именинников нет.')
        except KeyError:
            print('В записной книге пока ещё нет контактов с указанными датами рождения.')
    except json.decoder.JSONDecodeError:
        print('В записной книге пока ещё нет контактов.')

birthday_boys(file_name)
