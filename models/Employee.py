from . import DataBase
from . import Pharmacy

class Employee: 
    
    def __init__(self, id = False, code = False, name = False, lastname = False, address = False, role = False, pharmacy_id = False) -> None:
        self.id = id
        self.code = code 
        self.name = name 
        self.lastname = lastname 
        self.address = address
        self.role = role
        self.pharmacy_id = pharmacy_id
        
    def _get_all_employees(self, pharmacy_id): 
        employees = []
        
        data = DataBase().select_where("Employees", "employee_pharmacy_id", pharmacy_id)
        for employee in data: 
            employee_obj = Employee(*employee)
            employees.append(employee_obj)
        
        return employees
    
    def _get_filtered_employees(self, pharmacy_id, field, value): 
        employees = []
        fields = {
            'pharmacy_id' : pharmacy_id, 
            field : value,
        }
        
        data = DataBase().select_where_multiple_fields("Employees", "employee_", fields)
        for employee in data: 
            employee_obj = Employee(*employee)
            employees.append(employee_obj)
    
        return employees
    
    def _save_new(self): 
        DataBase().insert("employee_", "Employees", self)
        Pharmacy().add_n_employees(self.pharmacy_id)