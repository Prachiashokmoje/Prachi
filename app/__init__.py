from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    """Application factory function"""
    
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/mathlab.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.school import school_bp
    from app.routes.student import student_bp
    from app.routes.teacher import teacher_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(school_bp, url_prefix='/school')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Import models to ensure they are registered
        from app.models.user import User
        from app.models.school import School
        from app.models.class_model import Class
        from app.models.content import Content
        from app.models.progress import Progress
    
    return app