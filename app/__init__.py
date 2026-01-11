from flask import Flask
from config import db, migrate, Config

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    
    db.init_app(app)
    migrate.init_app(app, db)

    
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
