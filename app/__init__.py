import os
import sys

# Ensure directory structure exists
_current_dir = os.path.dirname(os.path.abspath(__file__))
_dirs = [
    os.path.join(_current_dir, 'core'),
    os.path.join(_current_dir, 'auth'),
    os.path.join(_current_dir, 'admin'),
    os.path.join(_current_dir, 'client'),
    os.path.join(_current_dir, 'customer'),
    os.path.join(_current_dir, 'templates'),
    os.path.join(_current_dir, 'templates', 'auth'),
    os.path.join(_current_dir, 'templates', 'admin'),
    os.path.join(_current_dir, 'templates', 'client'),
    os.path.join(_current_dir, 'templates', 'customer'),
    os.path.join(_current_dir, 'templates', 'components'),
]

for _dir in _dirs:
    os.makedirs(_dir, exist_ok=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name='development'):
    """Create and configure Flask app"""
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import config
    
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Import models to register them
    from app.models import User, Event, Ticket, Cancellation, Customer, Review, Payout, Admin
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints - these will be created later
    try:
        from app.auth.routes import auth_bp
        from app.admin.routes import admin_bp
        from app.client.routes import client_bp
        from app.customer.routes import customer_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(client_bp)
        app.register_blueprint(customer_bp)
    except ImportError:
        pass
    
    # Add home route
    @app.route('/')
    def home():
        from flask_login import current_user
        from flask import redirect, url_for
        if current_user.is_authenticated:
            if current_user.is_admin():
                return redirect(url_for('admin.dashboard'))
            elif current_user.is_client():
                return redirect(url_for('client.dashboard'))
            else:
                return redirect(url_for('customer.dashboard'))
        return redirect(url_for('auth.login'))
    
    return app
