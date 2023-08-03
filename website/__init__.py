from flask import Flask, request,  has_request_context
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
DB_NAME = "database.db"
logger = logging.getLogger()

class NewFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote = request.remote_addr
        else:
            record.url = None
            record.remote = None
        return super().format(record)
        

logFormatter = NewFormatter("%(asctime)s - %(url)s - %(remote)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# add console handler to the root logger
consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)

# add file handler to the root logger
fileHandler = RotatingFileHandler("logs.log", backupCount=100, maxBytes=1024)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'frgrdefvesfsadfe'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') # / for no prefix
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')