from . import DataBase

class Pharmacy:     
    
    def __init__(self, id = False, code = False, name = False, address = False, city = False, n_employees = False) -> None:
        self.id = id
        self.code = code
        self.name = name 
        self.address = address 
        self.city = city
        self.n_employees = n_employees
        
        
    def _get_all_pharmacies(self):
        pharmacies = []
        data = DataBase().select_all("Pharmacies")
        for pharmacy in data: 
            pharmacy_obj = Pharmacy(*pharmacy)
            pharmacies.append(pharmacy_obj)
            
        return pharmacies
    
    def _get_filtered_pharmacies(self, field, value): 
        pharmacies = []
        data = DataBase().select_where("Pharmacies", f"pharmacy_{field}", value)
        for pharmacy in data: 
            pharmacy_obj = Pharmacy(*pharmacy)
            pharmacies.append(pharmacy_obj)
            
        return pharmacies
    
    def _save_new_pharmacy(self): 
        DataBase().insert("pharmacy_", "Pharmacies", self)
        
        