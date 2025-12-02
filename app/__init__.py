from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main_bp.index' # If user is not logged in, send them to the main page
login_manager.login_message_category = 'info' 

# Flask-Login finds a user
@login_manager.user_loader
def load_user(user_id):
    from .models import User 
    return User.query.get(int(user_id))



def create_app():
    """Constructs the core application and its components."""
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = config.SECRET_KEY
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app) # Connect login manager

    with app.app_context():
        from . import routes
        from . import auth

        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp, url_prefix='/auth')

        # Create database tables
        db.create_all()

        # Create logs folder
        if not os.path.exists('logs'):
            os.makedirs('logs')

        return app
