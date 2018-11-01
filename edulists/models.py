import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from edulists import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), index=True, unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    password_hash = db.Column(db.String(256))
    state = db.Column(db.String(3))
    date_joined = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, email, first_name, last_name, state):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.state = state

    def __repr__(self):
        return f'<User {self.id}, {self.email}, {self.state}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash)