from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    """User model for authentication and role management"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # admin, school_admin, teacher, student
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    school = db.relationship('School', backref='users')
    class_assigned = db.relationship('Class', backref='students')
    progress_records = db.relationship('Progress', backref='student', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def is_school_admin(self):
        """Check if user is school admin"""
        return self.role == 'school_admin'
    
    def is_teacher(self):
        """Check if user is teacher"""
        return self.role == 'teacher'
    
    def is_student(self):
        """Check if user is student"""
        return self.role == 'student'
    
    def get_full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return User.query.get(int(user_id))