from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import User, ParkingLot, ParkingSpot, Reservation
from application.security import jwt
from flask_caching import Cache
from celery import Celery
from flask_mail import Mail, Message
from flask_cors import CORS

app = None
celery = None
cache = Cache()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    
    # Celery Configuration (use lowercase keys)
    app.config['broker_url'] = 'redis://localhost:6379/1'
    app.config['result_backend'] = 'redis://localhost:6379/2'

    db.init_app(app)
    jwt.init_app(app)
    
    # Flask-Mail configuration (example for Mailtrap)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'sharma001prateek@gmail.com'
    app.config['MAIL_PASSWORD'] = 'vxcd rrhq wfrw pkka'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    mail.init_app(app)
    
    # Initialize Cache
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
    cache.init_app(app)
    
    app.app_context().push()
    return app

app = create_app()

# Celery Initialization
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['result_backend'],
        broker=app.config['broker_url']
    )
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

# Import routes and tasks so Celery registers them
from application.routes import *
from application.tasks import *   # <-- This line is required

if __name__ == '__main__':
    app.run()
