from project import db, bcrypt
from project.messages.models import Message
from flask_login import UserMixin


class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    messages = db.relationship('Message', backref='user',lazy='dynamic')

    def __init__(self,username, password, email, first_name, last_name):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.email = email
        self.first_name = first_name
        self.last_name = last_name