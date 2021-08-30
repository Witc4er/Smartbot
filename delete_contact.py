from load_or_dump import load_note, dump_note 
import os


file_name = 'test.json'


def delete_contact():

    try:
        is_found = True
    
        if os.stat(file_name).st_size == 0:        # Проверяем пустой список или нет
            return print('empty')
        load_data = load_note(file_name) 
        contact_name = input("Enter contact's name to delete: " )
    
        for contact in load_data:
            if contact_name == contact['name']:
                is_found = False
                index = load_data.index(contact)
                load_data.pop(index)
                dump_note(file_name, load_data) 
                return print(f"Contact {contact_name} has been deleted")    
        if is_found:
            print(f"Contact {contact_name} not found")
            
    except FileNotFoundError:
        print("File not found")           
        
           

if __name__ == "__main__":
    delete_contact()