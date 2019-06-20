from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os

# ---------- [ App ] ---------- #
# start app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a76b5f023beafb12a665af6361491bbb'

basedir = os.path.abspath(os.path.dirname(__file__))

# ---------- [ Database ] ---------- #
# configure db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://eqzvuhka:nO6S59cLYCJrJbGh4pln0ryrhRegFrz7@hansken.db.elephantsql.com:5432/eqzvuhka'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize the db
db = SQLAlchemy(app)
# initialize marshmallow
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app import routes