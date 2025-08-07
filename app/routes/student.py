from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.content import Content
from app.models.progress import Progress
from app.models.class_model import Class
from app import db
from datetime import datetime
import json

student_bp = Blueprint('student', __name__)

def student_required(f):
    """Decorator to check if user is student"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_student():
            flash('Access denied. Student privileges required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    """Student dashboard"""
    # Get student's class
    class_obj = current_user.class_assigned
    
    # Get available content for student's grade
    if class_obj:
        available_content = Content.query.filter_by(
            grade=class_obj.grade,
            is_active=True
        ).all()
    else:
        available_content = []
    
    # Get student's progress
    progress_records = Progress.query.filter_by(student_id=current_user.id).all()
    
    # Calculate statistics
    total_content = len(available_content)
    completed_content = len([p for p in progress_records if p.completed])
    average_score = 0
    if completed_content > 0:
        total_score = sum([p.score for p in progress_records if p.completed and p.score])
        average_score = total_score / completed_content
    
    return render_template('student/dashboard.html',
                         class_obj=class_obj,
                         available_content=available_content,
                         progress_records=progress_records,
                         total_content=total_content,
                         completed_content=completed_content,
                         average_score=average_score)

@student_bp.route('/content')
@login_required
@student_required
def content():
    """Browse available content"""
    class_obj = current_user.class_assigned
    if not class_obj:
        flash('You are not assigned to any class.', 'warning')
        return redirect(url_for('student.dashboard'))
    
    content_list = Content.query.filter_by(
        grade=class_obj.grade,
        is_active=True
    ).order_by(Content.topic, Content.difficulty_level).all()
    
    return render_template('student/content.html', content_list=content_list)

@student_bp.route('/content/<int:content_id>')
@login_required
@student_required
def view_content(content_id):
    """View specific content"""
    content = Content.query.get_or_404(content_id)
    
    # Check if student has access to this content
    class_obj = current_user.class_assigned
    if not class_obj or content.grade != class_obj.grade:
        flash('Access denied to this content.', 'error')
        return redirect(url_for('student.content'))
    
    # Get or create progress record
    progress = Progress.query.filter_by(
        student_id=current_user.id,
        content_id=content_id
    ).first()
    
    if not progress:
        progress = Progress(
            student_id=current_user.id,
            content_id=content_id
        )
        db.session.add(progress)
        db.session.commit()
    
    return render_template('student/view_content.html', content=content, progress=progress)

@student_bp.route('/content/<int:content_id>/start')
@login_required
@student_required
def start_content(content_id):
    """Start working on content"""
    content = Content.query.get_or_404(content_id)
    progress = Progress.query.filter_by(
        student_id=current_user.id,
        content_id=content_id
    ).first()
    
    if progress:
        progress.started_at = datetime.utcnow()
        db.session.commit()
    
    return render_template('student/simulation.html', content=content, progress=progress)

@student_bp.route('/content/<int:content_id>/submit', methods=['POST'])
@login_required
@student_required
def submit_content(content_id):
    """Submit content completion"""
    data = request.get_json()
    
    progress = Progress.query.filter_by(
        student_id=current_user.id,
        content_id=content_id
    ).first()
    
    if progress:
        progress.score = data.get('score', 0)
        progress.completed = True
        progress.completed_at = datetime.utcnow()
        progress.time_spent = data.get('time_spent', 0)
        progress.correct_answers = data.get('correct_answers', 0)
        progress.total_questions = data.get('total_questions', 0)
        progress.calculate_score()
        progress.notes = data.get('notes', '')
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Progress saved successfully!'})
    
    return jsonify({'success': False, 'message': 'Progress record not found'})

@student_bp.route('/progress')
@login_required
@student_required
def progress():
    """View progress report"""
    progress_records = Progress.query.filter_by(student_id=current_user.id).all()
    
    # Group by topic
    topic_progress = {}
    for record in progress_records:
        topic = record.content.topic
        if topic not in topic_progress:
            topic_progress[topic] = []
        topic_progress[topic].append(record)
    
    return render_template('student/progress.html', topic_progress=topic_progress)

@student_bp.route('/profile')
@login_required
@student_required
def profile():
    """Student profile"""
    return render_template('student/profile.html')