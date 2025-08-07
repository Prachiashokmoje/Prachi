#!/usr/bin/env python3
"""
Setup script for Mathematics Lab application
This script initializes the database and creates sample data for testing
"""

import os
import sys
from app import create_app, db
from app.models.user import User
from app.models.school import School
from app.models.class_model import Class
from app.models.content import Content

def create_sample_data():
    """Create sample data for testing"""
    app = create_app()
    
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Create super admin
        admin = User(
            username='admin',
            email='admin@mathlab.com',
            first_name='Super',
            last_name='Admin',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample school
        school = School(
            name='Delhi Public School',
            address='123 Education Street',
            city='New Delhi',
            state='Delhi',
            pincode='110001',
            phone='011-12345678',
            email='info@dps.edu.in'
        )
        db.session.add(school)
        db.session.commit()
        
        # Create school admin
        school_admin = User(
            username='schooladmin',
            email='admin@dps.edu.in',
            first_name='School',
            last_name='Administrator',
            role='school_admin',
            school_id=school.id
        )
        school_admin.set_password('school123')
        db.session.add(school_admin)
        
        # Create sample teacher
        teacher = User(
            username='teacher1',
            email='teacher@dps.edu.in',
            first_name='Mathematics',
            last_name='Teacher',
            role='teacher',
            school_id=school.id
        )
        teacher.set_password('teacher123')
        db.session.add(teacher)
        
        # Create sample class
        class_10a = Class(
            name='Class 10A',
            grade=10,
            section='A',
            school_id=school.id,
            teacher_id=teacher.id
        )
        db.session.add(class_10a)
        
        # Create sample student
        student = User(
            username='student1',
            email='student@dps.edu.in',
            first_name='John',
            last_name='Doe',
            role='student',
            school_id=school.id,
            class_id=class_10a.id
        )
        student.set_password('student123')
        db.session.add(student)
        
        # Create sample content
        content1 = Content(
            title='Introduction to Quadratic Equations',
            description='Learn about quadratic equations and their solutions',
            grade=10,
            topic='Quadratic Equations',
            content_type='simulation',
            difficulty_level='beginner',
            instructions='Solve the quadratic equation step by step',
            learning_objectives='Understand quadratic equations and their solutions',
            estimated_duration=30,
            created_by=teacher.id
        )
        db.session.add(content1)
        
        content2 = Content(
            title='Basic Addition Practice',
            description='Practice basic addition with visual aids',
            grade=1,
            topic='Addition',
            content_type='activity',
            difficulty_level='beginner',
            instructions='Add the numbers using the number line',
            learning_objectives='Master basic addition skills',
            estimated_duration=15,
            created_by=teacher.id
        )
        db.session.add(content2)
        
        db.session.commit()
        
        print("✅ Sample data created successfully!")
        print("\n📋 Login Credentials:")
        print("Super Admin: admin / admin123")
        print("School Admin: schooladmin / school123")
        print("Teacher: teacher1 / teacher123")
        print("Student: student1 / student123")

def main():
    """Main setup function"""
    print("🚀 Setting up Mathematics Lab Application...")
    
    try:
        create_sample_data()
        print("\n🎉 Setup completed successfully!")
        print("\n📝 Next steps:")
        print("1. Run 'python main.py' to start the application")
        print("2. Open the application in your browser")
        print("3. Login with the provided credentials")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()