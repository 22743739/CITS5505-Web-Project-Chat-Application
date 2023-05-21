
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

import os
import datetime


# Create App
app = Flask(__name__, static_url_path='/static', template_folder='static')
app.debug = True

# Connect to database
db_file_path = os.path.abspath(os.getcwd()) + "/db/sqlite.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file_path
db = SQLAlchemy(app)

# Session
app.secret_key = "super secret key"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
session = Session(app)

# User Model


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    mobileNumber = db.Column(db.String)
    password = db.Column(db.String)
    createAt = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "mobileNumber": self.mobileNumber,
            "password": self.password,
            "createAt": self.createAt,
        }


# create Tables
# with app.app_context():
#     db.create_all()
