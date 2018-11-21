from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from edulists import db, config, login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), index=True, unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    ip_address = db.Column(db.String(32))
    password_hash = db.Column(db.String(256))
    is_superuser = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())

    # relationships
    subscriptions = db.relationship('Subscription', backref='user')

    def __init__(self, email, first_name, last_name, ip_address, is_superuser=False):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.ip_address = ip_address
        self.is_superuser = is_superuser

    def __repr__(self):
        return f'<User({self.id}, {self.email})>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Subject(db.Model):
    __tablename__ = 'subject'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    curriculum = db.Column(db.String(16))

    # relationships
    subscriptions = db.relationship('Subscription', backref='subject')

    def __init__(self, name, curriculum):
        self.name = name
        self.curriculum = curriculum

    def __repr__(self):
        return f'<Subject({self.id}, {self.curriculum})>'

    def has_subscriber(self, user_id):
        for subscription in self.subscriptions:
            if subscription.user_id == user_id:
                return True
        return False

    @property
    def address(self):
        address_curriculum = self.curriculum.lower()
        address_name = self.name.lower().replace(' ', '-')
        return f'{address_curriculum}-{address_name}'

class Subscription(db.Model):
    __tablename__ = 'subscription'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))

    def __init__(self, user_id, subject_id):
        self.user_id = user_id
        self.subject_id = subject_id

    def __repr__(self):
        return f'<Subject({self.id}, {self.user_id}, {self.subject_id})>'