from datetime import datetime, date


#На вход передаем список из нашего файла json
def birthday_boys(contacts):
    current_date = date.today()
    #Парсим список по записям
    for contact in contacts:
        #формируем новую дату др с актуальным годом
        new_bd_day = datetime.strptime(contact['birthday'], '%d.%m.%Y').day
        new_bd_month = datetime.strptime(contact['birthday'], '%d.%m.%Y').month
        new_bd = date(year=current_date.year, month=new_bd_month, day=new_bd_day)
        #считаем дельту между др и сегодня
        delta = new_bd-current_date
        #если дельта меньше 7 - отображаем в консоль имя: дата
        if delta.days < 7:
            print(f"{contact['name']}: {contact['birthday']}")
