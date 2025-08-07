from app import db
from datetime import datetime

class Content(db.Model):
    """Content model for mathematical content, simulations, and activities"""
    
    __tablename__ = 'content'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    grade = db.Column(db.Integer, nullable=False)  # 1-12
    topic = db.Column(db.String(100), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # simulation, activity, exercise, lesson
    difficulty_level = db.Column(db.String(20), default='beginner')  # beginner, intermediate, advanced
    file_path = db.Column(db.String(500), nullable=True)  # Path to content files
    html_content = db.Column(db.Text, nullable=True)  # HTML content for simulations
    js_code = db.Column(db.Text, nullable=True)  # JavaScript code for interactivity
    css_styles = db.Column(db.Text, nullable=True)  # CSS styles
    instructions = db.Column(db.Text, nullable=True)  # Instructions for students
    learning_objectives = db.Column(db.Text, nullable=True)  # Learning objectives
    prerequisites = db.Column(db.Text, nullable=True)  # Prerequisites
    estimated_duration = db.Column(db.Integer, nullable=True)  # Duration in minutes
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by])
    progress_records = db.relationship('Progress', backref='content', lazy='dynamic')
    
    def get_content_type_display(self):
        """Get human-readable content type"""
        types = {
            'simulation': 'Interactive Simulation',
            'activity': 'Hands-on Activity',
            'exercise': 'Practice Exercise',
            'lesson': 'Lesson Content',
            'quiz': 'Assessment Quiz',
            'worksheet': 'Worksheet'
        }
        return types.get(self.content_type, self.content_type.title())
    
    def get_difficulty_color(self):
        """Get color class for difficulty level"""
        colors = {
            'beginner': 'success',
            'intermediate': 'warning',
            'advanced': 'danger'
        }
        return colors.get(self.difficulty_level, 'secondary')
    
    def get_completion_rate(self):
        """Get completion rate for this content"""
        total_attempts = self.progress_records.count()
        if total_attempts == 0:
            return 0
        completed = self.progress_records.filter_by(completed=True).count()
        return (completed / total_attempts) * 100
    
    def get_average_score(self):
        """Get average score for this content"""
        records = self.progress_records.filter_by(completed=True).all()
        if not records:
            return 0
        total_score = sum(record.score for record in records)
        return total_score / len(records)
    
    def __repr__(self):
        return f'<Content {self.title}>'