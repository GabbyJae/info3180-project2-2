from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"

######################
#   DATABASE CONFIG  #
######################
user = 'postgres'
password = 'XPostgresia!123'
database = 'Photogram'
######################


UPLOAD_FOLDER = './app/static/uploads'

app.config['SECRET_KEY'] = "this is a super secret key"  # you should make this more random and unique
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://%s:%s@localhost/%s" % (user,password,database)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:ilovemilk18@localhost/Photogram"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # added just to suppress a warning
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



db = SQLAlchemy(app)


app.config.from_object(__name__)
from app import views
