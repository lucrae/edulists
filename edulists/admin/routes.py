from flask import Blueprint, render_template, flash, redirect, url_for

from edulists import db
from edulists.models import User, Subject, Subscription

admin = Blueprint('admin', __name__)

@admin.route('/')
def index():
    return render_template('admin/index.html')

