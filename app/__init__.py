from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_login import LoginManager
from flask_cache import Cache
import redis


db = MongoEngine()
login = LoginManager()
login.login_view = 'login'
bootstrap = Bootstrap()
cache = Cache(config={'CACHE_TYPE': 'simple'})
redis_pool = redis.ConnectionPool(host=Config.REDIS_SETTINGS['host'],
                                  port=Config.REDIS_SETTINGS['port'],
                                  decode_responses=False)
place_redis = redis.Redis(connection_pool=redis_pool)


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    db.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
        from app.admin import bp as admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.place import bp as place_bp
    app.register_blueprint(place_bp)

    return app

from app import models
