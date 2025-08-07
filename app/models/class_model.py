from app import db
from datetime import datetime

class Class(db.Model):
    """Class model for managing grade levels and classes"""
    
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # e.g., "Class 1A", "Grade 10B"
    grade = db.Column(db.Integer, nullable=False)  # 1-12 for CBSE grades
    section = db.Column(db.String(10), nullable=True)  # A, B, C, etc.
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    academic_year = db.Column(db.String(20), nullable=False, default='2024-25')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    teacher = db.relationship('User', foreign_keys=[teacher_id])
    students = db.relationship('User', backref='class_assigned', lazy='dynamic')
    
    def get_display_name(self):
        """Get formatted class name"""
        if self.section:
            return f"Class {self.grade}{self.section}"
        return f"Class {self.grade}"
    
    def get_student_count(self):
        """Get number of students in the class"""
        return self.students.count()
    
    def get_grade_level(self):
        """Get grade level description"""
        if self.grade <= 5:
            return "Primary"
        elif self.grade <= 8:
            return "Middle"
        elif self.grade <= 10:
            return "Secondary"
        else:
            return "Higher Secondary"
    
    def get_cbse_topics(self):
        """Get CBSE topics for this grade"""
        topics = {
            1: ["Numbers", "Addition", "Subtraction", "Shapes", "Measurement"],
            2: ["Numbers", "Addition", "Subtraction", "Multiplication", "Shapes", "Money"],
            3: ["Numbers", "Addition", "Subtraction", "Multiplication", "Division", "Fractions", "Money", "Time"],
            4: ["Numbers", "Addition", "Subtraction", "Multiplication", "Division", "Fractions", "Decimals", "Money", "Time", "Geometry"],
            5: ["Numbers", "Fractions", "Decimals", "Money", "Time", "Geometry", "Measurement", "Data Handling"],
            6: ["Number System", "Algebra", "Geometry", "Mensuration", "Data Handling"],
            7: ["Number System", "Algebra", "Geometry", "Mensuration", "Data Handling"],
            8: ["Number System", "Algebra", "Geometry", "Mensuration", "Data Handling"],
            9: ["Number Systems", "Algebra", "Coordinate Geometry", "Geometry", "Mensuration", "Statistics", "Probability"],
            10: ["Real Numbers", "Polynomials", "Pair of Linear Equations", "Quadratic Equations", "Arithmetic Progressions", "Triangles", "Coordinate Geometry", "Introduction to Trigonometry", "Some Applications of Trigonometry", "Circles", "Constructions", "Areas Related to Circles", "Surface Areas and Volumes", "Statistics", "Probability"],
            11: ["Sets", "Relations and Functions", "Trigonometric Functions", "Complex Numbers and Quadratic Equations", "Linear Inequalities", "Permutations and Combinations", "Binomial Theorem", "Sequences and Series", "Straight Lines", "Conic Sections", "Introduction to Three-dimensional Geometry", "Limits and Derivatives", "Mathematical Reasoning", "Statistics", "Probability"],
            12: ["Relations and Functions", "Inverse Trigonometric Functions", "Matrices", "Determinants", "Continuity and Differentiability", "Application of Derivatives", "Integrals", "Application of Integrals", "Differential Equations", "Vector Algebra", "Three Dimensional Geometry", "Linear Programming", "Probability"]
        }
        return topics.get(self.grade, [])
    
    def __repr__(self):
        return f'<Class {self.get_display_name()}>'