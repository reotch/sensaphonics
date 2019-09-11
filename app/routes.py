from flask import render_template, url_for, request, jsonify, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import Product, ProductSchema, Customer, Order, product_schema, products_schema
from flask_login import login_user, current_user, logout_user, login_required

# ---------- [ Home and Customer Routes ] ---------- #
# server/
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

# Customer Registration Route
''' 
This registration takes in user registration, adds and commits it to the database. 
The user registers and is returned to the login screen to log in.
'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = Customer(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, phone_number = form.phone_number.data, password = hashed_pw)
        db.session.add(customer)
        db.session.commit()
        flash('Account created. You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Customer login
'''
This route will login the user and redirect them to the index ('home') page.
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:
            flash('Nope. Try checking your email and password')
    return render_template('login.html', title='Login', form=form)

# Customer logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Customer view account
@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

# ---------- [ PRODUCT ROUTES ] ----------- #
# GET all IEMs
@app.route('/iems', methods=['GET'])
def products():
    iems = Product.query.all()
    return render_template('iems.html', products=iems)

# GET single IEM
@app.route('/iems/<id>', methods=['GET'])
def product(id):
    iem = Product.query.get(id)
    return render_template('iems.html', products=iem)

@app.route('/about')
def about():
    return render_template('about.html')