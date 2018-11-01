import configparser

# read in config file
config_file = configparser.ConfigParser()
config_file.readfp(open(r'config.cfg'))

class Config:
    SECRET_KEY = config_file.get('general', 'SECRET_KEY')

    # database
    DB_USER = config_file.get('database', 'USER')
    DB_PASSWORD = config_file.get('database', 'PASSWORD')
    DB_ADDRESS = config_file.get('database', 'ADDRESS')
    DB_NAME = config_file.get('database', 'NAME')
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False