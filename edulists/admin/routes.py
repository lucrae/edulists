from flask import Blueprint, render_template, current_app

admin = Blueprint('admin', __name__)

@admin.route('/')
def index():
    config_details = {
        'server': {
            'name': current_app.name,
            'secret_key': '*'*len(current_app.config['SECRET_KEY']),
            'environment': current_app.config['ENV'],
            'debug': current_app.config['DEBUG'],
            'testing': current_app.config['TESTING'],
            'application_root': current_app.config['APPLICATION_ROOT'],
        },
        'cookies': {
            'name': current_app.config['SESSION_COOKIE_NAME'],
            'http_only': current_app.config['SESSION_COOKIE_HTTPONLY'],
            'refresh_each_request': current_app.config['SESSION_REFRESH_EACH_REQUEST'],

        },
        'database': {
            'name': current_app.config['DB_NAME'],
            'address': current_app.config['DB_ADDRESS'],
            'user': current_app.config['DB_USER'],
            'password': '*'*len(current_app.config['DB_PASSWORD']),
            'binds': current_app.config['SQLALCHEMY_BINDS'],
            'track_modifcations': current_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'],
            'commit_on_teardown': current_app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'],
        }
    }

    return render_template('admin/index.html', config_details=config_details)