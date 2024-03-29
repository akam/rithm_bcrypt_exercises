from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_modus import Modus
import os
from flask_login import LoginManager


app = Flask(__name__)
bcrypt = Bcrypt(app)
modus = Modus(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/learn-auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'seriously, set a super secret key' # bad practice in general, but we'll live with it for now
db = SQLAlchemy(app)


from project.users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')

login_manager.login_view = "users.login"

from project.users.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def index():
    return redirect(url_for('users.login'))