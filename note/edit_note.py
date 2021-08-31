from load_or_dump import load_note, dump_note 
import os


file_name = 'test.json'

    

def edit_note():

    try:
        is_found = True
    
        if os.stat(file_name).st_size == 0:      # Проверяем пустой список или нет
            return print('empty')
        load_data = load_note(file_name) 
        note_name = input("Enter note's title to edit: " )
    
        for note in load_data:
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
                
                dump_note(file_name, load_data) 
                print(f"Note {note_name} has been edited")    
        if is_found:
            print(f"Note {note_name} not found")

    except FileNotFoundError:
        print("File not found")  
            
                   
           

if __name__ == "__main__":
    edit_note()