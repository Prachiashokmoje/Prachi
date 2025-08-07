from app import db
from datetime import datetime

class Progress(db.Model):
    """Progress model for tracking student progress and performance"""
    
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    score = db.Column(db.Float, nullable=True)  # Score as percentage
    max_score = db.Column(db.Float, default=100.0)
    completed = db.Column(db.Boolean, default=False)
    time_spent = db.Column(db.Integer, nullable=True)  # Time spent in seconds
    attempts = db.Column(db.Integer, default=1)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    feedback = db.Column(db.Text, nullable=True)  # Teacher feedback
    notes = db.Column(db.Text, nullable=True)  # Student notes
    
    # Additional fields for detailed tracking
    correct_answers = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=0)
    accuracy = db.Column(db.Float, nullable=True)  # Percentage of correct answers
    
    def calculate_score(self):
        """Calculate score percentage"""
        if self.total_questions > 0:
            self.score = (self.correct_answers / self.total_questions) * 100
            self.accuracy = self.score
        return self.score
    
    def mark_completed(self):
        """Mark content as completed"""
        self.completed = True
        self.completed_at = datetime.utcnow()
    
    def get_time_spent_formatted(self):
        """Get formatted time spent"""
        if not self.time_spent:
            return "N/A"
        
        minutes = self.time_spent // 60
        seconds = self.time_spent % 60
        
        if minutes > 0:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"
    
    def get_score_color(self):
        """Get color class based on score"""
        if not self.score:
            return 'secondary'
        elif self.score >= 90:
            return 'success'
        elif self.score >= 70:
            return 'info'
        elif self.score >= 50:
            return 'warning'
        else:
            return 'danger'
    
    def get_performance_level(self):
        """Get performance level description"""
        if not self.score:
            return 'Not Attempted'
        elif self.score >= 90:
            return 'Excellent'
        elif self.score >= 80:
            return 'Very Good'
        elif self.score >= 70:
            return 'Good'
        elif self.score >= 60:
            return 'Satisfactory'
        elif self.score >= 50:
            return 'Needs Improvement'
        else:
            return 'Poor'
    
    def __repr__(self):
        return f'<Progress Student:{self.student_id} Content:{self.content_id}>'