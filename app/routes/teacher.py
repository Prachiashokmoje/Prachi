from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.class_model import Class
from app.models.user import User
from app.models.content import Content
from app.models.progress import Progress
from app import db
from datetime import datetime

teacher_bp = Blueprint('teacher', __name__)

def teacher_required(f):
    """Decorator to check if user is teacher"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_teacher():
            flash('Access denied. Teacher privileges required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    """Teacher dashboard"""
    # Get classes taught by this teacher
    classes = Class.query.filter_by(teacher_id=current_user.id).all()
    
    # Get total students
    total_students = 0
    for class_obj in classes:
        total_students += class_obj.get_student_count()
    
    # Get recent student activities
    recent_activities = []
    for class_obj in classes:
        class_activities = Progress.query.join(User).filter(
            User.class_id == class_obj.id
        ).order_by(Progress.completed_at.desc()).limit(5).all()
        recent_activities.extend(class_activities)
    
    # Sort by completion date
    recent_activities.sort(key=lambda x: x.completed_at or datetime.min, reverse=True)
    recent_activities = recent_activities[:10]
    
    return render_template('teacher/dashboard.html',
                         classes=classes,
                         total_students=total_students,
                         recent_activities=recent_activities)

@teacher_bp.route('/classes')
@login_required
@teacher_required
def classes():
    """List classes taught by teacher"""
    classes = Class.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/classes.html', classes=classes)

@teacher_bp.route('/classes/<int:class_id>')
@login_required
@teacher_required
def class_details(class_id):
    """View class details and students"""
    class_obj = Class.query.get_or_404(class_id)
    
    # Check if teacher teaches this class
    if class_obj.teacher_id != current_user.id:
        flash('Access denied to this class.', 'error')
        return redirect(url_for('teacher.classes'))
    
    students = User.query.filter_by(class_id=class_id, role='student').all()
    
    return render_template('teacher/class_details.html', class_obj=class_obj, students=students)

@teacher_bp.route('/classes/<int:class_id>/students')
@login_required
@teacher_required
def class_students(class_id):
    """View students in a class with their progress"""
    class_obj = Class.query.get_or_404(class_id)
    
    # Check if teacher teaches this class
    if class_obj.teacher_id != current_user.id:
        flash('Access denied to this class.', 'error')
        return redirect(url_for('teacher.classes'))
    
    students = User.query.filter_by(class_id=class_id, role='student').all()
    
    # Get progress for each student
    student_progress = {}
    for student in students:
        progress_records = Progress.query.filter_by(student_id=student.id).all()
        completed = len([p for p in progress_records if p.completed])
        total = len(progress_records)
        average_score = 0
        if completed > 0:
            scores = [p.score for p in progress_records if p.completed and p.score]
            if scores:
                average_score = sum(scores) / len(scores)
        
        student_progress[student.id] = {
            'completed': completed,
            'total': total,
            'average_score': average_score,
            'progress_records': progress_records
        }
    
    return render_template('teacher/class_students.html', 
                         class_obj=class_obj, 
                         students=students,
                         student_progress=student_progress)

@teacher_bp.route('/students/<int:student_id>/progress')
@login_required
@teacher_required
def student_progress(student_id):
    """View detailed progress of a specific student"""
    student = User.query.get_or_404(student_id)
    
    # Check if student is in teacher's class
    if not student.class_assigned or student.class_assigned.teacher_id != current_user.id:
        flash('Access denied to this student.', 'error')
        return redirect(url_for('teacher.classes'))
    
    progress_records = Progress.query.filter_by(student_id=student_id).all()
    
    # Group by topic
    topic_progress = {}
    for record in progress_records:
        topic = record.content.topic
        if topic not in topic_progress:
            topic_progress[topic] = []
        topic_progress[topic].append(record)
    
    return render_template('teacher/student_progress.html', 
                         student=student,
                         topic_progress=topic_progress)

@teacher_bp.route('/content')
@login_required
@teacher_required
def content():
    """Browse content for teacher's classes"""
    classes = Class.query.filter_by(teacher_id=current_user.id).all()
    grades = list(set([c.grade for c in classes]))
    
    content_list = Content.query.filter(
        Content.grade.in_(grades),
        Content.is_active == True
    ).order_by(Content.grade, Content.topic).all()
    
    return render_template('teacher/content.html', content_list=content_list)

@teacher_bp.route('/content/create', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_content():
    """Create new content"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        grade = request.form.get('grade')
        topic = request.form.get('topic')
        content_type = request.form.get('content_type')
        difficulty_level = request.form.get('difficulty_level')
        instructions = request.form.get('instructions')
        learning_objectives = request.form.get('learning_objectives')
        estimated_duration = request.form.get('estimated_duration')
        
        content = Content(
            title=title,
            description=description,
            grade=grade,
            topic=topic,
            content_type=content_type,
            difficulty_level=difficulty_level,
            instructions=instructions,
            learning_objectives=learning_objectives,
            estimated_duration=estimated_duration,
            created_by=current_user.id
        )
        
        db.session.add(content)
        db.session.commit()
        
        flash('Content created successfully!', 'success')
        return redirect(url_for('teacher.content'))
    
    classes = Class.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/create_content.html', classes=classes)

@teacher_bp.route('/reports')
@login_required
@teacher_required
def reports():
    """Teacher reports"""
    classes = Class.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/reports.html', classes=classes)