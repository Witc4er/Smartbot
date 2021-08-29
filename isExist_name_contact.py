from load_or_dump import load_note, dump_note 
import os


file_name = 'test.json'


def isExist_name_contact(contact_name):

    try:
        is_found = True
    
        if os.stat(file_name).st_size == 0:        # Проверяем пустой список или нет
            return print('empty')
        load_data = load_note(file_name) 
    
        for contact in load_data:
            if contact_name == contact['name']:
                is_found = False
                check1 = input("Contact's name is exist. Are you editing or creating a contact? edit_contact/add_contact: ")
                if check1 == 'edit_contact':
                # edit_contact()
                    print("Contact has been edited")
                elif check1 == 'add_contact':
                # edit_contact()
                    print("Contact has been added")
                   
        if is_found:
            print(f"Contact {contact_name} not found")
            
    except FileNotFoundError:
        print("File not found")           
        
           

if __name__ == "__main__":
    isExist_name_contact()