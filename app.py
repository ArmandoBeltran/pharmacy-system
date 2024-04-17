from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

from models import Pharmacy, Laboratory, Product, Employee, StockLine

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#Pharmacies routes
@app.route('/pharmacies')
def get_pharmacies():
    pharmacies = Pharmacy()._get_all_pharmacies()
    filters = {
        'code' : "Clave", 
        'name' : "Nombre",
        'address' : "Dirección",
        'city' : "Ciudad", 
        'n_employees' : "Número de empleados"
    }
    
    return render_template('modules/pharmacies/list.html', pharmacies = pharmacies, filters = filters)

@app.route('/filtered-pharmacies', methods=['POST'])
def get_filtered_pharmacies():
    field = request.form.get('filters')
    value = request.form.get('search_text')
    
    pharmacies = Pharmacy()._get_filtered_pharmacies(field, value)
    filters = {
        'code' : "Clave", 
        'name' : "Nombre",
        'address' : "Dirección",
        'city' : "Ciudad", 
        'n_employees' : "Número de empleados"
    }
    return render_template('modules/pharmacies/list.html', pharmacies = pharmacies, filters = filters)

@app.route('/pharmacies-form')
def pharmacies_form():
    return render_template('modules/pharmacies/form.html')

@app.route('/create-new-pharmacy', methods=['POST'])
def create_new_pharmacy():
    code = request.form.get('code')
    name = request.form.get('name')
    address = request.form.get('address')
    city = request.form.get('city')
    
    new_pharmacy = Pharmacy(False, code, name, address, city, 0)
    new_pharmacy._save_new_pharmacy()
    
    return redirect(url_for('pharmacies_form'))

#Employee routes
@app.route('/employees', methods=['GET'])
def get_employees():
    pharmacies = Pharmacy()._get_all_pharmacies()
    filters = {
        'code' : "Clave", 
        'name' : "Nombre",
        'lastname' : "Apellido",
        'address' : "Dirección", 
        'role' : "Posición", 
        'pharmacy_id' : "Farmacia"
    }
    
    pharmacies = {
        pharmacy.id : {
            'name' : pharmacy.name, 
            'employees' : [employee for employee in Employee()._get_all_employees(pharmacy.id)]
        }
        for pharmacy in pharmacies
    }
    
    return render_template('modules/employees/list.html', pharmacies = pharmacies, filters = filters)

@app.route('/filtered-employees', methods=['POST'])
def get_filtered_employees():
    field = request.form.get('filters')
    value = request.form.get('search_text')
    
    if field == "pharmacy_id":
        pharmacies = Pharmacy()._get_filtered_pharmacies("name", value)
        pharmacies = {
            pharmacy.id : {
                'name' : pharmacy.name, 
                'employees' : [employee for employee in Employee()._get_all_employees(pharmacy.id)]
            }
            for pharmacy in pharmacies
        }
    else: 
        pharmacies = Pharmacy()._get_all_pharmacies()
        pharmacies = {
            pharmacy.id : {
                'name' : pharmacy.name, 
                'employees' : [employee for employee in Employee()._get_filtered_employees(pharmacy.id, field, value)]
            }
            for pharmacy in pharmacies
        }
    
    filters = {
        'code' : "Clave", 
        'name' : "Nombre",
        'lastname' : "Apellido",
        'address' : "Dirección", 
        'role' : "Posición", 
        'pharmacy_id' : "Farmacia"
    }
    
    return render_template('modules/employees/list.html', pharmacies = pharmacies, filters = filters)
    

@app.route('/employees-form')
def employees_form():
    pharmacies = Pharmacy()._get_all_pharmacies()
    return render_template('modules/employees/form.html', pharmacies = pharmacies)

@app.route('/create-new-employee', methods=['POST'])
def create_new_employee():
    code = request.form.get("code")
    name = request.form.get("name")
    lastname = request.form.get("lastname")
    address = request.form.get("address")
    role = request.form.get("role")
    pharmacy_id = request.form.get("pharmacy")
    
    new_employee = Employee(False, code, name, lastname, address, role, pharmacy_id)
    new_employee._save_new()
    
    return redirect(url_for("employees_form"))
    

#Stock_line routes
@app.route('/stock-lines')
def get_stock_lines():
    pharmacies = Pharmacy()._get_all_pharmacies()
    products   = Product()._get_all_products()

    filters = {
        'name' : "Folio",
        'date' : "Fecha", 
        'stock': "Cantidad", 
        'product_id': "Producto", 
        'pharmacy_id': "Farmacia"
    }
    
    pharmacies = {
        pharmacy.id : {
            'name' : pharmacy.name, 
            'products' : {
                product.id : {
                    'name' : f"{product.name} - {product.presentation}",
                    'lines': [stock_line for stock_line in StockLine()._get_lines_(pharmacy.id, product.id)]
                }
                for product in products
            }
        }
        for pharmacy in pharmacies
    }
    
    return render_template('modules/stock_lines/list.html', pharmacies = pharmacies, filters = filters)

@app.route('/filtered-stock-lines', methods=['POST'])
def get_filtered_stock_lines():
    field = request.form.get('filters')
    value = request.form.get('search_text')
    
    filters = {
        'name' : "Folio",
        'date' : "Fecha", 
        'stock': "Cantidad", 
        'product_id': "Producto", 
        'pharmacy_id': "Farmacia"
    }
    
    if field == "pharmacy_id":
        pharmacies = Pharmacy()._get_filtered_pharmacies("name", value)
        products   = Product()._get_all_products()
        pharmacies = {
            pharmacy.id : {
                'name' : pharmacy.name, 
                'products' : {
                    product.id : {
                        'name' : f"{product.name} - {product.presentation}",
                        'lines': [stock_line for stock_line in StockLine()._get_lines_(pharmacy.id, product.id)]
                    }
                    for product in products
                }
            }
            for pharmacy in pharmacies
        }
    elif field == "product_id": 
        pharmacies = Pharmacy()._get_all_pharmacies()
        products = Product()._get_filtered_products("name", value)
        pharmacies = {
            pharmacy.id : {
                'name' : pharmacy.name, 
                'products' : {
                    product.id : {
                        'name' : f"{product.name} - {product.presentation}",
                        'lines': [stock_line for stock_line in StockLine()._get_lines_(pharmacy.id, product.id)]
                    }
                    for product in products
                }
            }
            for pharmacy in pharmacies
        }
    else: 
        pharmacies = Pharmacy()._get_all_pharmacies()
        products = Product()._get_all_products()
        pharmacies = {
            pharmacy.id : {
                'name' : pharmacy.name, 
                'products' : {
                    product.id : {
                        'name' : f"{product.name} - {product.presentation}",
                        'lines': [stock_line for stock_line in StockLine()._get_filtered_lines(pharmacy.id, product.id, field, value)]
                    }
                    for product in products
                }
            }
            for pharmacy in pharmacies
        }
    
    return render_template('modules/stock_lines/list.html', pharmacies = pharmacies, filters = filters)

@app.route('/stock-lines-form')
def stock_lines_form():
    pharmacies = Pharmacy()._get_all_pharmacies()
    products = Product()._get_all_products()
    return render_template('modules/stock_lines/form.html', pharmacies = pharmacies, products = products)

@app.route('/create-new-stock-line', methods=['POST'])
def create_new_stock_line():
    name = request.form.get('name')
    date = request.form.get('date')
    stock = float(request.form.get('stock'))
    product_id = request.form.get('product')
    pharmacy_id = request.form.get('pharmacy')
    
    new_stock_line = StockLine(False, name, date, stock, product_id, pharmacy_id)
    new_stock_line._save_new()
    
    return redirect(url_for('stock_lines_form'))

#Product routes
@app.route('/products')
def get_products():
    products = Product()._get_all_products()
    filters = {
        'reference' : "Clave", 
        'name' : "Nombre",
        'presentation' : "Presentación",
        'price' : "Precio", 
        'therapeutic_actions' : "Acción terapéutica", 
        'laboratory_id' : "Laboratorio"
    }
    
    return render_template('modules/products/list.html', products = products, filters = filters)

@app.route('/filtered-products', methods=['POST'])
def get_filtered_products():
    field = request.form.get('filters')
    value = request.form.get('search_text')
    
    if field == "laboratory_id":
        products = Product()._get_filtered_products_by_lab(field, value)
    else:  
        products = Product()._get_filtered_products(field, value)
        
    filters = {
        'reference' : "Clave", 
        'name' : "Nombre",
        'presentation' : "Presentación",
        'price' : "Precio", 
        'therapeutic_actions' : "Acción terapéutica", 
        'laboratory_id' : "Laboratorio"
    }
    
    return render_template('modules/products/list.html', products = products, filters = filters)

@app.route('/products-form')
def products_form():
    laboratories = Laboratory()._get_all_laboratories()
    return render_template('modules/products/form.html', laboratories = laboratories)

@app.route('/create-new-product', methods=['POST'])
def create_new_product():
    reference = request.form.get("reference")
    name = request.form.get("name")
    presentation = request.form.get("presentation")
    price = request.form.get("price")
    therapeutic_actions = request.form.get("therapeutic_actions")
    laboratory_id = request.form.get("laboratory")
    
    new_product = Product(False, reference, name, presentation, price, therapeutic_actions, laboratory_id)
    new_product._save_new_product()
    
    return redirect(url_for('products_form'))

#Laboratory routes
@app.route('/laboratories')
def get_laboratories():
    laboratories = Laboratory()._get_all_laboratories()
    filters = {
        'name' : 'Nombre', 
        'address' : 'Dirección', 
        'phone' : 'Teléfono'
    }
    
    return render_template('modules/laboratories/list.html', laboratories = laboratories, filters = filters)

@app.route('/filtered-laboratories', methods=['POST'])
def get_filtered_laboratories():
    field = request.form.get("filters")
    value = request.form.get("search_text")
    
    laboratories = Laboratory()._get_filtered_laboratories(field, value)
    filters = {
        'name' : 'Nombre', 
        'address' : 'Dirección', 
        'phone' : 'Teléfono'
    }
    
    return render_template('modules/laboratories/list.html', laboratories = laboratories, filters = filters)
    
@app.route('/laboratories-form')
def laboratories_form():
    return render_template('modules/laboratories/form.html')

@app.route('/create-new-laboratory', methods=['POST'])
def create_new_laboratory():
    name = request.form.get("name")
    address = request.form.get("address")
    phone = request.form.get("phone")
    
    new_laboratory = Laboratory(False, name, address, phone)
    new_laboratory._save_new_laboratory()
    
    return redirect(url_for("laboratories_form"))

app.run(debug=True)