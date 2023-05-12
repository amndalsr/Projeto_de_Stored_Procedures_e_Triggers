from flask import render_template, request, redirect, url_for, session
from app import app, db
from app.models import Customer, Category, Product
from sqlalchemy import text

@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('index.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    customer_id = request.form['CustomerID']
    company_name = request.form['CompanyName']
    contact_name = request.form['ContactName']
    contact_title = request.form['ContactTitle']
    address = request.form['Address']
    city = request.form['City']
    region = request.form['Region']
    postal_code = request.form['PostalCode']
    country = request.form['Country']
    phone = request.form['Phone']
    fax = request.form['Fax']
    new_customer = Customer(CustomerID=customer_id, CompanyName=company_name, ContactName=contact_name, ContactTitle=contact_title, Address=address, City=city, Region=region, PostalCode=postal_code, Country=country, Phone=phone, Fax=fax)
    db.session.add(new_customer)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete_customer/<CustomerID>', methods=['POST'])
def delete_customer(CustomerID):
    customer = Customer.query.get(CustomerID)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return "Erro: Cliente não encontrado", 404

@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/category/<int:CategoryID>')
def category(CategoryID):
    category = Category.query.get(CategoryID)
    products = Product.query.filter_by(CategoryID=CategoryID).all()
    return render_template('category.html', category=category, products=products)

def update_cart_total():
    session['cart_total'] = sum(product['price'] for product in session['cart'])

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(product.serialize())
    update_cart_total()
    session.modified = True

    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:index>', methods=['GET'])
def remove_from_cart(index):
    if 0 <= index < len(session['cart']):
        session['cart'].pop(index)
        update_cart_total()
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    if 'cart' not in session:
        session['cart'] = []
    return render_template('cart.html', cart=session['cart'])

