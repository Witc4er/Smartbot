import json


def dump_note(path_file, new_data):
    
    with open(path_file, 'w') as fh:
        json.dump(new_data, fh)


def load_note(path_file):
    
    with open(path_file, 'r') as fh:
        load_data = json.load(fh)
        
        return load_data  

       