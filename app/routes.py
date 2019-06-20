from flask import render_template, url_for, request, jsonify, flash, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import Product, ProductSchema, Customer, Order
from flask_login import login_user

# ---------- [ Routes ] ---------- #
# server/
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

# Create Registration Route
''' This registration takes in user registration, adds and commits it to the database. The user registers and is returned to the login screen to log in.'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = Customer(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, phone_number = form.phone_number.data, password = hashed_pw)
        db.session.add(customer)
        db.session.commit()
        flash('Account created. You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

'''This route will login the user and redirect them to the index ('home') page'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # if form.email.data == 'xenu@sea.org' and form.password.data == 'password':
        #     flash('Logged in and schitt')
        #     return redirect(url_for('index'))
        # else:
        customer = Customer.query.filter_by(email = form.email.data).first()
        if customer and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer)
            return redirect(url_for('index'))
        else:
            flash('Nope. Try checking your email and password')
    return render_template('login.html', title='Login', form=form)

# Create API route for creating product
@app.route('/iems', methods = ['GET'])
def add_product():
    model = request.json['model']
    description = request.json['description']
    price = request.json['price']

    # initialize product with info
    new_product = Product(model, description, price)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

@app.route('/about')
def about():
    return render_template('about.html')