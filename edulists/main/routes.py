from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import urllib3

from edulists import db
from edulists.models import User
from edulists.forms import RegisterForm, LoginForm

http = urllib3.PoolManager()

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_anonymous:
        return redirect(url_for('main.subjects'))

    form = RegisterForm()

    if form.validate_on_submit():

        # create new user
        new_user = User(
            form.email.data,
            form.first_name.data.title(),
            form.last_name.data.title(),
            http.request('GET', 'http://ip.42.pl/raw').data.decode('utf-8'),
        )

        # create user password
        new_user.set_password(form.password.data)

        # add user to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('MSG_REG', 'success')
        return redirect(url_for('main.index'))

    return render_template('main/index.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():

    # user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():

        # log user in
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=form.remember_me.data)

        flash('You are now logged in.', 'success')
        return redirect(url_for('main.index'))

    return render_template('main/login.html', title='Login', form=form)

@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        new_user = User(
            form.email.data,
            form.first_name.data.title(),
            form.last_name.data.title(),
            urllib.request.urlopen('http://ip.42.pl/raw').read().decode('utf-8'),
        )

        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()
        
        flash('MSG_REG', 'success')
        return redirect(url_for('main.register'))

    return render_template('main/register.html', title='Register', form=form)

@main.route('/subjects')
@login_required
def subjects():
    return render_template('main/subjects.html', title='Subjects')

@main.route('/about')
def about():
    return render_template('main/about.html', title='About')

@main.route('/terms')
def terms():
    return render_template('main/terms.html', title='Terms of Service')