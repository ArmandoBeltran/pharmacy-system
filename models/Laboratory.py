from . import DataBase

class Laboratory: 
    
    def __init__(self, id = False, name = False, address = False, phone = False) -> None:
        self.id = id 
        self.name = name 
        self.address = address 
        self.phone = phone
        
    def _get_all_laboratories(self): 
        laboratories = []
        data = DataBase().select_all("Laboratories")
        for laboratory in data: 
            laboratory_obj = Laboratory(*laboratory)
            laboratories.append(laboratory_obj)
        
        return laboratories
    
    def _get_filtered_laboratories(self, field, value): 
        laboratories = []
        data = DataBase().select_where("Laboratories", field, value)
        for laboratory in data: 
            laboratory_obj = Laboratory(*laboratory)
            laboratories.append(laboratory_obj)
        
        return laboratories
    
    def _save_new_laboratory(self): 
        DataBase().insert("laboratory_", "Laboratories", self)