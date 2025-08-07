from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.school import School
from app.models.user import User
from app.models.class_model import Class
from app import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to check if user is admin"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    total_schools = School.query.count()
    total_users = User.query.count()
    total_students = User.query.filter_by(role='student').count()
    total_teachers = User.query.filter_by(role='teacher').count()
    
    recent_schools = School.query.order_by(School.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_schools=total_schools,
                         total_users=total_users,
                         total_students=total_students,
                         total_teachers=total_teachers,
                         recent_schools=recent_schools)

@admin_bp.route('/schools')
@login_required
@admin_required
def schools():
    """List all schools"""
    schools = School.query.all()
    return render_template('admin/schools.html', schools=schools)

@admin_bp.route('/schools/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_school():
    """Create a new school"""
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        pincode = request.form.get('pincode')
        phone = request.form.get('phone')
        email = request.form.get('email')
        
        school = School(
            name=name,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            phone=phone,
            email=email
        )
        
        db.session.add(school)
        db.session.commit()
        
        flash('School created successfully!', 'success')
        return redirect(url_for('admin.schools'))
    
    return render_template('admin/create_school.html')

@admin_bp.route('/schools/<int:school_id>')
@login_required
@admin_required
def school_details(school_id):
    """View school details"""
    school = School.query.get_or_404(school_id)
    return render_template('admin/school_details.html', school=school)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """List all users"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    """System reports"""
    return render_template('admin/reports.html')