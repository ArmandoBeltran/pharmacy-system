from .DataBase import DataBase

class StockLine(): 
    
    def __init__(self, id = False, name = False, date = False, stock = False, product_id = False, pharmacy_id = False) -> None:
        self.name = name
        self.date = date
        self.stock = stock
        self.product_id = product_id
        self.pharmacy_id = pharmacy_id
        
    def _get_lines_(self, pharmacy_id, product_id): 
        stock_lines = []
        fields = {
            'pharmacy_id' : pharmacy_id, 
            'product_id'  : product_id, 
        }
        data = DataBase().select_where_multiple_fields('Stock_lines', 'stock_line_', fields)
        for stock_line in data: 
            stock_line_obj = StockLine(*stock_line)
            stock_lines.append(stock_line_obj)
        
        return stock_lines
    
    def _get_filtered_lines(self, pharmacy_id, product_id, field, value): 
        stock_lines = []
        fields = {
            'pharmacy_id' : pharmacy_id, 
            'product_id'  : product_id, 
            field : value
        }
        data = DataBase().select_where_multiple_fields('Stock_lines', 'stock_line_', fields)
        for stock_line in data: 
            stock_line_obj = StockLine(*stock_line)
            stock_lines.append(stock_line_obj)
        
        return stock_lines
        
    def _save_new(self): 
        DataBase().insert("stock_line_", "Stock_Lines", self)