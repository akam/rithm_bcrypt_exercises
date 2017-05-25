from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()
modus = Modus(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
login_manager.login_view = "users.login"

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'Implement me later please'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/users-blueprints'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# import a blueprint that we will create
from project.users.views import users_blueprint
from project.messages.views import messages_blueprint
from project.users.models import User
# register our blueprints with the application
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(messages_blueprint, url_prefix='/users/<int:id>/messages')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def root():
    return "HELLO BLUEPRINTS!"