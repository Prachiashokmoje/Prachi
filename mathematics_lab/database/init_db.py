"""
Database initialization script for Mathematics Lab application.
Creates initial superadmin user and sample data.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from .models import db_manager
from ..auth.authentication import auth_manager


def create_initial_superadmin():
    """Create the initial superadmin user."""
    try:
        # Check if superadmin already exists
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'superadmin'")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count > 0:
            print("SuperAdmin already exists. Skipping creation.")
            return
        
        # Create superadmin
        superadmin_data = auth_manager.register_user(
            username="superadmin",
            email="admin@mathematicslab.com",
            password="Admin123!",
            first_name="System",
            last_name="Administrator",
            role="superadmin"
        )
        
        print(f"SuperAdmin created successfully!")
        print(f"Username: {superadmin_data['username']}")
        print(f"Email: {superadmin_data['email']}")
        print("Password: Admin123!")
        print("\nPlease change the password after first login.")
        
    except Exception as e:
        print(f"Error creating superadmin: {e}")


def create_sample_schools():
    """Create sample schools for testing."""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Check if schools already exist
        cursor.execute("SELECT COUNT(*) FROM schools")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("Sample schools already exist. Skipping creation.")
            conn.close()
            return
        
        # Create sample schools
        sample_schools = [
            {
                'name': 'Delhi Public School',
                'address': '123 Education Street, New Delhi',
                'contact_email': 'info@dps.edu.in',
                'contact_phone': '+91-11-12345678'
            },
            {
                'name': 'Kendriya Vidyalaya',
                'address': '456 Learning Avenue, Mumbai',
                'contact_email': 'principal@kv.edu.in',
                'contact_phone': '+91-22-87654321'
            },
            {
                'name': 'St. Mary\'s Convent School',
                'address': '789 Knowledge Road, Bangalore',
                'contact_email': 'admin@stmarys.edu.in',
                'contact_phone': '+91-80-11223344'
            }
        ]
        
        for school in sample_schools:
            cursor.execute('''
                INSERT INTO schools (name, address, contact_email, contact_phone)
                VALUES (?, ?, ?, ?)
            ''', (school['name'], school['address'], school['contact_email'], school['contact_phone']))
        
        conn.commit()
        conn.close()
        print("Sample schools created successfully!")
        
    except Exception as e:
        print(f"Error creating sample schools: {e}")


def create_sample_users():
    """Create sample users for testing."""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Get school IDs
        cursor.execute("SELECT id FROM schools LIMIT 3")
        school_ids = [row[0] for row in cursor.fetchall()]
        
        if not school_ids:
            print("No schools found. Please create schools first.")
            conn.close()
            return
        
        # Sample users data
        sample_users = [
            # School Admin for first school
            {
                'username': 'schooladmin1',
                'email': 'admin@dps.edu.in',
                'password': 'Admin123!',
                'first_name': 'School',
                'last_name': 'Admin',
                'role': 'schooladmin',
                'school_id': school_ids[0]
            },
            # Teacher for first school
            {
                'username': 'teacher1',
                'email': 'teacher@dps.edu.in',
                'password': 'Teacher123!',
                'first_name': 'Mathematics',
                'last_name': 'Teacher',
                'role': 'teacher',
                'school_id': school_ids[0]
            },
            # Student for first school
            {
                'username': 'student1',
                'email': 'student@dps.edu.in',
                'password': 'Student123!',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'student',
                'school_id': school_ids[0]
            }
        ]
        
        for user_data in sample_users:
            try:
                auth_manager.register_user(**user_data)
                print(f"Created user: {user_data['username']} ({user_data['role']})")
            except Exception as e:
                print(f"Error creating user {user_data['username']}: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error creating sample users: {e}")


def main():
    """Main initialization function."""
    print("Initializing Mathematics Lab Database...")
    print("=" * 50)
    
    # Create initial superadmin
    print("\n1. Creating SuperAdmin...")
    create_initial_superadmin()
    
    # Create sample schools
    print("\n2. Creating sample schools...")
    create_sample_schools()
    
    # Create sample users
    print("\n3. Creating sample users...")
    create_sample_users()
    
    print("\n" + "=" * 50)
    print("Database initialization completed!")
    print("\nDefault login credentials:")
    print("SuperAdmin: superadmin / Admin123!")
    print("SchoolAdmin: schooladmin1 / Admin123!")
    print("Teacher: teacher1 / Teacher123!")
    print("Student: student1 / Student123!")


if __name__ == "__main__":
    main()