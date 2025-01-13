from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

nag = Flask(__name__)
nag.config['SECRET_KEY'] = "ASDASD5REFSD432SD;"
nag.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
nag.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db = SQLAlchemy(nag)
login_manager = LoginManager(nag)
login_manager.login_view = "login"

