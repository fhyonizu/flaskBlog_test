from flask import Flask
from .views import *
from .exts import init_exts, db


def create_app():

    app = Flask(__name__)
    app.secret_key = 'asdfghjkl1234567890'
    app.register_blueprint(blueprint=blue)

    # db_uri = 'sqlite:///sqlite3.db'
    db_uri = 'mysql+pymysql://blog:fhyoni@150.158.124.90:3306/blog?charset=utf8mb4'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_timeout': 30  # 设置超时时间为30秒
    }

    init_exts(app)

    with app.app_context():
        db.create_all()

    return app