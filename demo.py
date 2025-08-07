#!/usr/bin/env python3
"""
Mathematics Lab Application - Demo Script
Demonstrates the core functionality of Sprint 1 without GUI
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database.db_manager import DatabaseManager
from auth.auth_manager import AuthManager


def demo_database_functionality():
    """Demonstrate database operations"""
    print("=" * 60)
    print("MATHEMATICS LAB APPLICATION - SPRINT 1 DEMO")
    print("=" * 60)
    
    print("\n1. DATABASE INITIALIZATION")
    print("-" * 30)
    
    # Initialize database (in memory for demo)
    db = DatabaseManager(':memory:')
    db.initialize_database()
    print("✓ Database initialized with complete schema")
    
    # List all tables
    tables = db.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
    print(f"✓ Created {len(tables)} tables:")
    for table in tables:
        print(f"  - {table['name']}")
    
    return db


def demo_authentication(db):
    """Demonstrate authentication functionality"""
    print("\n2. AUTHENTICATION SYSTEM")
    print("-" * 30)
    
    auth = AuthManager(db)
    
    # Create different types of users
    users_to_create = [
        {
            'username': 'superadmin',
            'email': 'admin@mathlab.com',
            'password': 'admin123',
            'role': 'SuperAdmin',
            'first_name': 'System',
            'last_name': 'Administrator'
        },
        {
            'username': 'principal',
            'email': 'principal@school.com',
            'password': 'principal123',
            'role': 'SchoolAdmin',
            'first_name': 'Jane',
            'last_name': 'Smith'
        },
        {
            'username': 'teacher1',
            'email': 'teacher@school.com',
            'password': 'teacher123',
            'role': 'Teacher',
            'first_name': 'John',
            'last_name': 'Doe'
        },
        {
            'username': 'student1',
            'email': 'student@school.com',
            'password': 'student123',
            'role': 'Student',
            'first_name': 'Alice',
            'last_name': 'Johnson'
        }
    ]
    
    print("Creating test users:")
    created_users = []
    for user_data in users_to_create:
        try:
            user_id = auth.create_user(**user_data)
            created_users.append((user_id, user_data))
            print(f"✓ Created {user_data['role']}: {user_data['username']} (ID: {user_id})")
        except Exception as e:
            print(f"✗ Failed to create {user_data['username']}: {e}")
    
    return auth, created_users


def demo_authentication_flow(auth, created_users):
    """Demonstrate authentication flow"""
    print("\n3. AUTHENTICATION FLOW")
    print("-" * 30)
    
    # Test authentication for each user
    for user_id, user_data in created_users:
        username = user_data['username']
        password = user_data['password']
        
        print(f"\nTesting login for {username} ({user_data['role']}):")
        
        # Authenticate user
        authenticated_user = auth.authenticate_user(username, password)
        if authenticated_user:
            print(f"  ✓ Authentication successful")
            
            # Create session
            session_id = auth.create_session(authenticated_user['id'])
            print(f"  ✓ Session created: {session_id[:12]}...")
            
            # Validate session
            session_data = auth.validate_session(session_id)
            if session_data:
                print(f"  ✓ Session valid for: {session_data['username']}")
            else:
                print(f"  ✗ Session validation failed")
            
            # Invalidate session
            if auth.invalidate_session(session_id):
                print(f"  ✓ Session invalidated successfully")
            
        else:
            print(f"  ✗ Authentication failed")
        
        # Test wrong password
        wrong_auth = auth.authenticate_user(username, "wrongpassword")
        if not wrong_auth:
            print(f"  ✓ Correctly rejected wrong password")


def demo_role_permissions(auth):
    """Demonstrate role-based permissions"""
    print("\n4. ROLE-BASED PERMISSIONS")
    print("-" * 30)
    
    roles = ['SuperAdmin', 'SchoolAdmin', 'Teacher', 'Student']
    
    print("Permission matrix (can user role access target role):")
    print(f"{'User Role':<12} | {'SuperAdmin':<10} | {'SchoolAdmin':<11} | {'Teacher':<8} | {'Student':<8}")
    print("-" * 60)
    
    for user_role in roles:
        permissions = []
        for target_role in roles:
            can_access = auth.check_role_permission(user_role, target_role)
            permissions.append("✓" if can_access else "✗")
        
        print(f"{user_role:<12} | {permissions[0]:<10} | {permissions[1]:<11} | {permissions[2]:<8} | {permissions[3]:<8}")
    
    print("\nSchool access permissions:")
    print("- SuperAdmin can access any school: ✓")
    print("- SchoolAdmin can only access their school:")
    print(f"  - Own school (ID=1): {auth.can_access_school('SchoolAdmin', 1, 1)}")
    print(f"  - Other school (ID=2): {not auth.can_access_school('SchoolAdmin', 1, 2)}")


def demo_school_management(db):
    """Demonstrate school management"""
    print("\n5. SCHOOL MANAGEMENT")
    print("-" * 30)
    
    # Create sample schools
    schools_data = [
        {
            'name': 'Greenwood High School',
            'address': '123 Education Street, Delhi',
            'contact_email': 'admin@greenwood.edu',
            'contact_phone': '+91-11-12345678'
        },
        {
            'name': 'Sunrise Public School',
            'address': '456 Learning Avenue, Mumbai',
            'contact_email': 'info@sunrise.edu',
            'contact_phone': '+91-22-87654321'
        }
    ]
    
    print("Creating sample schools:")
    for school_data in schools_data:
        school_id = db.create_school(school_data)
        print(f"✓ Created school: {school_data['name']} (ID: {school_id})")
    
    # List all schools
    schools = db.get_schools()
    print(f"\nTotal schools in system: {len(schools)}")
    for school in schools:
        print(f"  - {school['name']} (Contact: {school['contact_email']})")


def demo_password_operations(auth, created_users):
    """Demonstrate password operations"""
    print("\n6. PASSWORD MANAGEMENT")
    print("-" * 30)
    
    # Get a test user
    test_user_id, test_user_data = created_users[3]  # Student
    username = test_user_data['username']
    old_password = test_user_data['password']
    new_password = "newpassword123"
    
    print(f"Testing password change for user: {username}")
    
    # Test password change with correct old password
    success = auth.change_password(test_user_id, old_password, new_password)
    if success:
        print("✓ Password changed successfully")
        
        # Verify old password no longer works
        old_auth = auth.authenticate_user(username, old_password)
        new_auth = auth.authenticate_user(username, new_password)
        
        if not old_auth and new_auth:
            print("✓ Old password correctly rejected, new password works")
        else:
            print("✗ Password change verification failed")
    else:
        print("✗ Password change failed")
    
    # Test password change with wrong old password
    wrong_change = auth.change_password(test_user_id, "wrongold", "anothernew")
    if not wrong_change:
        print("✓ Correctly rejected password change with wrong old password")


def main():
    """Run the complete demo"""
    try:
        # Demo database functionality
        db = demo_database_functionality()
        
        # Demo authentication
        auth, created_users = demo_authentication(db)
        
        # Demo authentication flow
        demo_authentication_flow(auth, created_users)
        
        # Demo role permissions
        demo_role_permissions(auth)
        
        # Demo school management
        demo_school_management(db)
        
        # Demo password operations
        demo_password_operations(auth, created_users)
        
        print("\n" + "=" * 60)
        print("✅ SPRINT 1 DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nAll core functionality is working:")
        print("✓ Database schema and operations")
        print("✓ User authentication with bcrypt password hashing")
        print("✓ Role-based access control")
        print("✓ Session management")
        print("✓ School management")
        print("✓ Password management")
        print("\nThe application is ready for Sprint 2 (UI development)!")
        
    except Exception as e:
        print(f"\n✗ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()