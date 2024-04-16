CREATE TABLE Pharmacies(
    pharmacy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pharmacy_code TEXT, 
    pharmacy_name TEXT, 
    pharmacy_address TEXT,
    pharmacy_city TEXT,
    pharmacy_n_employees INTEGER
); 

CREATE TABLE Laboratories(
    laboratory_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    laboratory_name TEXT, 
    laboratory_address TEXT, 
    laboratory_phone TEXT
); 

CREATE TABLE Products(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_reference TEXT, 
    product_name TEXT, 
    product_presentation TEXT, 
    product_price REAL, 
    product_therapeutic_actions TEXT,
    laboratory_id  INTEGER, 
    FOREIGN KEY(laboratory_id) REFERENCES Laboratories(laboratory_id)
); 
CREATE TABLE Employees(
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_code TEXT, 
    employee_name TEXT, 
    employee_lastname TEXT, 
    employee_address TEXT,
    employee_role TEXT,
    employee_pharmacy_id INTEGER,
    FOREIGN KEY(employee_pharmacy_id) REFERENCES Pharmacies(pharmacy_id) 
); 

CREATE TABLE Stock_lines(
    stock_line_id INTEGER PRIMARY KEY AUTOINCREMENT,  
    stock_line_name TEXT, 
    stock_line_date TEXT, 
    stock_line_stock REAL, 
    stock_line_product_id INTEGER,
    stock_line_pharmacy_id INTEGER,
    FOREIGN KEY(stock_line_product_id) REFERENCES Products(product_id)
    FOREIGN KEY(stock_line_pharmacy_id) REFERENCES Pharmacies(pharmacy_id)
); 