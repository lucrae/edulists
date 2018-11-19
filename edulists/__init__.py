from flask import Flask
from flask.cli import FlaskGroup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from edulists.config import Config

# define components
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'

# import blueprint groups
from edulists.main.routes import main
from edulists.admin.routes import admin

def create_app(config_class=Config):

    # create app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init components
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # register blueprints
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')

    return app