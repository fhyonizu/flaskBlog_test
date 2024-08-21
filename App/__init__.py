from flask import Flask
from .views import blue
from .exts import init_exts, db


def create_app():
    app = Flask(__name__)

    app.register_blueprint(blueprint=blue)

    # db_uri = 'sqlite:///sqlite3.db'
    db_uri = 'mysql+pymysql://root:root@127.0.0.1:3306/blog?charset=utf8mb4'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_exts(app)

    with app.app_context():
        db.create_all()

    return app