from app import db, ma, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(customer_id):
    return Customer.query.get(int(customer_id))

# ---------- [ Models ] ---------- #
# create models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    # qty = db.Column(db.Integer)

    def __init__(self, model, description, price):
        self.model = model
        self.description = description
        self.price = price
    
# Product Schema using Marshmallow to serialize
class ProductSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'model', 'description', 'price')

# initialize Schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    transaction_id = db.relationship('Order', backref = 'transaction number', lazy = 'dynamic')

    # def is_active(self):
    #     return True

    def __repr__(self):
        return f"Customer('{self.first_name} {self.last_name}')"

class Order(db.Model):
    #instantiate Customer inside order to make properties


    id = db.Column(db.Integer, primary_key=True)
    # QUESTION: Is this going to work? The columns referenced are in a different model
    transaction_id = db.Column(db.Integer, db.ForeignKey('customer.id'), unique=True)
    # need to make this a random generated number