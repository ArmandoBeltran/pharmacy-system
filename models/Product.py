from . import DataBase
from . import Laboratory

class Product: 
    
    def __init__(self, id = False, reference = False, name = False, presentation = False, price = False, therapeutic_actions = False, laboratory_id = False) -> None:
        self.id = id
        self.reference = reference
        self.name = name
        self.presentation = presentation
        self.price = price 
        self.therapeutic_actions = therapeutic_actions
        self.laboratory_id = laboratory_id
        
    def _get_laboratory(self, id): 
        laboratory = Laboratory()._get_filtered_laboratories("laboratory_id", id)[0]

        return laboratory
        
    def _get_all_products(self): 
        products = []
        data = DataBase().select_all("Products")
        for product in data:
            laboratory_id = product[6]
            laboratory = self._get_laboratory(laboratory_id)
            product_obj = Product(*product[:6], laboratory)
            products.append(product_obj)
        
        return products
    
    def _get_filtered_products(self, field, value): 
        products = []
        data = DataBase().select_where("Products", f"product_{field}", value)
        for product in data: 
            laboratory_id = product[6]
            laboratory = self._get_laboratory(laboratory_id)
            product_obj = Product(*product[:6], laboratory)
            products.append(product_obj)
            
        return products
    
    def _get_filtered_products_by_lab(self, field, value): 
        products = []
        tables = {
            'Products' : "product_", 
            'Laboratories': "laboratory_"
        }
        
        data = DataBase().select_multiple_tables(tables, field, value)
        for product in data: 
            laboratory_id = product[6]
            laboratory = self._get_laboratory(laboratory_id)
            product_obj = Product(*product[:6], laboratory)
            products.append(product_obj)
            
        return products
    
    def _save_new_product(self): 
        DataBase().insert("product_", "Products", self)
        
    