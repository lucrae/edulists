from flask import Flask
from flask.cli import FlaskGroup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from edulists.config import Config

# blueprint groups
from edulists.main.routes import main
from edulists.admin.routes import admin

# define components
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):

    # create app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init components
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')

    return app