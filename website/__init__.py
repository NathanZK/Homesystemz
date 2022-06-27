from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "smarthome.db"


def create_app():
    app = Flask(__name__)
    #app.config['SECRET_KEY'] = 'KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://gmiuwyarbzhxpo:d2b15818e1cc4d1be91eec6724c12789956f56206e189a3f1128343a7719bcf6@ec2-23-23-182-238.compute-1.amazonaws.com:5432/d60micc32r7opg'
    app.config['SECRET_KEY'] = 'KEY'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Room

    #create_database(app)

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
