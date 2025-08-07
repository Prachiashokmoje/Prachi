from app import db
from datetime import datetime

class School(db.Model):
    """School model for educational institutions"""
    
    __tablename__ = 'schools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    admin = db.relationship('User', foreign_keys=[admin_id])
    classes = db.relationship('Class', backref='school', lazy='dynamic')
    
    def get_full_address(self):
        """Get complete school address"""
        return f"{self.address}, {self.city}, {self.state} - {self.pincode}"
    
    def get_teacher_count(self):
        """Get number of teachers in the school"""
        from app.models.user import User
        return User.query.filter_by(school_id=self.id, role='teacher').count()
    
    def get_student_count(self):
        """Get number of students in the school"""
        from app.models.user import User
        return User.query.filter_by(school_id=self.id, role='student').count()
    
    def __repr__(self):
        return f'<School {self.name}>'