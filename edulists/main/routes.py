from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import urllib3

from edulists import db
from edulists.models import User, Subject, Subscription
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
        return redirect(url_for('main.index'))

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
            http.request('GET', 'http://ip.42.pl/raw').data.decode('utf-8'),
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
    subjects = [sub.subject for sub in current_user.subscriptions]

    curriculums = [
        {
            'name': 'Australian Curriculum',
            'acronym': 'GEN',
            'region': 'AUS',
            'years': 'F-10',
        },
        {
            'name': 'Victorian Certificate of Education',
            'acronym': 'VCE',
            'region': 'VIC',
            'years': '11-12',
        },
        {
            'name': 'Higher School Certificate',
            'acronym': 'HSC',
            'region': 'NSW',
            'years': '11-12',
        },
        {
            'name': 'Queensland Certificate of Education',
            'acronym': 'QCE',
            'region': 'QLD',
            'years': '11-12',
        }
    ]

    return render_template('main/subjects.html', title='Subjects', subjects=subjects, curriculums=curriculums)

@main.route('/browse-subjects/<curriculum>')
@login_required
def browse_subjects(curriculum):
    subjects = Subject.query.filter_by(curriculum=curriculum).all()

    return render_template('main/browse_subjects.html', title='Browse Subjects', curriculum=curriculum, subjects=subjects)

@main.route('/subscribe/<subject_id>')
@login_required
def subscribe(subject_id):
    subject = Subject.query.get(subject_id)
    
    # create subscription
    new_subscription = Subscription(current_user.id, subject_id)
    db.session.add(new_subscription)
    db.session.commit()

    flash(f'You are now subscribed to "{subject.curriculum}: {subject.name}"', 'success')

    # redirect back to page
    return redirect(url_for('main.browse_subjects', curriculum=subject.curriculum))

@main.route('/unsubscribe/<subject_id>')
@login_required
def unsubscribe(subject_id):
    subject = Subject.query.get(subject_id)
    subscription = Subscription.query.filter_by(user_id=current_user.id).filter_by(subject_id=subject_id)

    # delete the subscription
    subscription.delete()
    db.session.commit()

    flash(f'You have unsubscribed to "{subject.curriculum}: {subject.name}"', 'success')

    return redirect(url_for('main.browse_subjects', curriculum=subject.curriculum))

@main.route('/unsubscribe-from-subjects-page/<subject_id>')
@login_required
def unsubscribe_from_subjects_page(subject_id):
    subject = Subject.query.get(subject_id)
    subscription = Subscription.query.filter_by(user_id=current_user.id).filter_by(subject_id=subject_id)

    # delete the subscription
    subscription.delete()
    db.session.commit()

    flash(f'You have unsubscribed to "{subject.curriculum}: {subject.name}"', 'success')

    return redirect(url_for('main.subjects'))
        

@main.route('/about')
def about():
    return render_template('main/about.html', title='About')

@main.route('/terms')
def terms():
    return render_template('main/terms.html', title='Terms of Service')