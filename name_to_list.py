def load_names(file_path):
    with open(file_path,'r') as file:
        names_list=[line.strip() for line in file]
        return names_list
    
names=load_names('names.txt')

def is_it_name(name)->bool:
    names=load_names('names.txt')

    
    if name in names:
        return True
    else:
        return False
    