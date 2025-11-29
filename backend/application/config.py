class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///vechicle_parking_app_V2.sqlite3'
    JWT_SECRET_KEY = 'my_secret_key'