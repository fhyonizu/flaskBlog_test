from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_socketio import SocketIO, send, emit, join_room, leave_room

db = SQLAlchemy()
migrate = Migrate()
cache = Cache(config={'CACHE_TYPE': 'simple'})
socketio = SocketIO()
def init_exts(app):
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    socketio.init_app(app)