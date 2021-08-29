from load_or_dump import load_note, dump_note 
import os


file_name = 'test.json'


def delete_note():

    try:
        is_found = True
    
        if os.stat(file_name).st_size == 0:        # Проверяем пустой список или нет
            return print('empty')
        load_data = load_note(file_name) 
        note_title = input("Enter note's title to delete: " )
    
        for note in load_data:
            if note_title == note['name']:
                is_found = False
                index = load_data.index(note)
                load_data.pop(index)
                dump_note(file_name, load_data) 
                return print(f"Note {note_title} has been deleted")    
        if is_found:
            print(f"Note {note_title} not found")
            
    except FileNotFoundError:
        print("File not found")           
        
           

if __name__ == "__main__":
    delete_note()