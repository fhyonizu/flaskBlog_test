from flask import Flask
from .views import *
from .exts import init_exts, db


def create_app():

    app = Flask(__name__)
    app.register_blueprint(blueprint=blue)

    # db_uri = 'sqlite:///sqlite3.db'
    db_uri = 'mysql+pymysql://blog:fhyoni@150.158.124.90:3306/blog?charset=utf8mb4'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,  # 确保连接有效性
        'pool_timeout': 30,  # 设置超时时间为30秒
        'pool_size': 10,  # 设置连接池大小为10
        'max_overflow': 20,  # 允许连接池溢出20个连接
    }
    app.config['SECRET_KEY'] = 'awdfgc2323231ef'

    init_exts(app)

    with app.app_context():
        db.create_all()

    return app