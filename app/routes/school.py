from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.school import School
from app.models.user import User
from app.models.class_model import Class
from app.models.progress import Progress
from app import db
from datetime import datetime

school_bp = Blueprint('school', __name__)

def school_admin_required(f):
    """Decorator to check if user is school admin"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_school_admin():
            flash('Access denied. School admin privileges required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@school_bp.route('/dashboard')
@login_required
@school_admin_required
def dashboard():
    """School admin dashboard"""
    school = current_user.school
    total_teachers = User.query.filter_by(school_id=school.id, role='teacher').count()
    total_students = User.query.filter_by(school_id=school.id, role='student').count()
    total_classes = Class.query.filter_by(school_id=school.id).count()
    
    recent_activities = Progress.query.join(User).filter(
        User.school_id == school.id
    ).order_by(Progress.completed_at.desc()).limit(10).all()
    
    return render_template('school/dashboard.html',
                         school=school,
                         total_teachers=total_teachers,
                         total_students=total_students,
                         total_classes=total_classes,
                         recent_activities=recent_activities)

@school_bp.route('/teachers')
@login_required
@school_admin_required
def teachers():
    """List teachers in the school"""
    teachers = User.query.filter_by(school_id=current_user.school_id, role='teacher').all()
    return render_template('school/teachers.html', teachers=teachers)

@school_bp.route('/teachers/create', methods=['GET', 'POST'])
@login_required
@school_admin_required
def create_teacher():
    """Create a new teacher account"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('school/create_teacher.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('school/create_teacher.html')
        
        teacher = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='teacher',
            school_id=current_user.school_id
        )
        teacher.set_password(password)
        
        db.session.add(teacher)
        db.session.commit()
        
        flash('Teacher account created successfully!', 'success')
        return redirect(url_for('school.teachers'))
    
    return render_template('school/create_teacher.html')

@school_bp.route('/students')
@login_required
@school_admin_required
def students():
    """List students in the school"""
    students = User.query.filter_by(school_id=current_user.school_id, role='student').all()
    return render_template('school/students.html', students=students)

@school_bp.route('/students/create', methods=['GET', 'POST'])
@login_required
@school_admin_required
def create_student():
    """Create a new student account"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        class_id = request.form.get('class_id')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('school/create_student.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('school/create_student.html')
        
        student = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='student',
            school_id=current_user.school_id,
            class_id=class_id
        )
        student.set_password(password)
        
        db.session.add(student)
        db.session.commit()
        
        flash('Student account created successfully!', 'success')
        return redirect(url_for('school.students'))
    
    classes = Class.query.filter_by(school_id=current_user.school_id).all()
    return render_template('school/create_student.html', classes=classes)

@school_bp.route('/classes')
@login_required
@school_admin_required
def classes():
    """List classes in the school"""
    classes = Class.query.filter_by(school_id=current_user.school_id).all()
    return render_template('school/classes.html', classes=classes)

@school_bp.route('/classes/create', methods=['GET', 'POST'])
@login_required
@school_admin_required
def create_class():
    """Create a new class"""
    if request.method == 'POST':
        name = request.form.get('name')
        grade = request.form.get('grade')
        section = request.form.get('section')
        teacher_id = request.form.get('teacher_id')
        
        class_obj = Class(
            name=name,
            grade=grade,
            section=section,
            school_id=current_user.school_id,
            teacher_id=teacher_id
        )
        
        db.session.add(class_obj)
        db.session.commit()
        
        flash('Class created successfully!', 'success')
        return redirect(url_for('school.classes'))
    
    teachers = User.query.filter_by(school_id=current_user.school_id, role='teacher').all()
    return render_template('school/create_class.html', teachers=teachers)

@school_bp.route('/reports')
@login_required
@school_admin_required
def reports():
    """School reports"""
    return render_template('school/reports.html')