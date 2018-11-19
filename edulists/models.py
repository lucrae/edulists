from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from edulists import db, config, login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), index=True, unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    ip_address = db.Column(db.String(32))
    password_hash = db.Column(db.String(256))
    is_superuser = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, email, first_name, last_name, ip_address, is_superuser=False):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.ip_address = ip_address
        self.is_superuser = is_superuser

    def __repr__(self):
        return f'<User {self.id}, {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)