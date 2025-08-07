#!/usr/bin/env python3
"""
Test script for Sprint 1 functionality.
"""

import sys
import os
from pathlib import Path

# Add the mathematics_lab directory to the Python path
sys.path.append(str(Path(__file__).parent / "mathematics_lab"))

def test_database_initialization():
    """Test database initialization."""
    print("Testing database initialization...")
    
    try:
        from mathematics_lab.database.models import db_manager
        
        # Test database connection
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN (
                'users', 'schools', 'classes', 'topics', 'lessons', 
                'activities', 'activity_attempts', 'student_progress', 'sessions'
            )
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        expected_tables = [
            'users', 'schools', 'classes', 'topics', 'lessons',
            'activities', 'activity_attempts', 'student_progress', 'sessions'
        ]
        
        conn.close()
        
        if set(tables) == set(expected_tables):
            print("✅ Database initialization successful - all tables created")
            return True
        else:
            print("❌ Database initialization failed - missing tables")
            print(f"Expected: {expected_tables}")
            print(f"Found: {tables}")
            return False
            
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False


def test_authentication():
    """Test authentication functionality."""
    print("\nTesting authentication...")
    
    try:
        from mathematics_lab.auth.authentication import auth_manager, AuthenticationError
        
        # Test password hashing
        password = "TestPassword123!"
        hashed = auth_manager.hash_password(password)
        
        if auth_manager.verify_password(password, hashed):
            print("✅ Password hashing and verification working")
        else:
            print("❌ Password hashing failed")
            return False
        
        # Test password validation
        is_valid, message = auth_manager.validate_password(password)
        if is_valid:
            print("✅ Password validation working")
        else:
            print(f"❌ Password validation failed: {message}")
            return False
        
        # Test email validation
        if auth_manager.validate_email("test@example.com"):
            print("✅ Email validation working")
        else:
            print("❌ Email validation failed")
            return False
        
        # Test user registration
        user_data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'ValidPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'student'
        }
        
        user = auth_manager.register_user(**user_data)
        if user['username'] == user_data['username']:
            print("✅ User registration working")
        else:
            print("❌ User registration failed")
            return False
        
        # Test user login
        login_result = auth_manager.login('testuser2', 'ValidPass123!')
        if login_result['user']['username'] == 'testuser2':
            print("✅ User login working")
        else:
            print("❌ User login failed")
            return False
        
        # Test role-based access
        session_token = login_result['session_token']
        user = auth_manager.require_student(session_token)
        if user['role'] == 'student':
            print("✅ Role-based access control working")
        else:
            print("❌ Role-based access control failed")
            return False
        
        # Test logout
        if auth_manager.logout(session_token):
            print("✅ User logout working")
        else:
            print("❌ User logout failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False


def test_database_initialization_script():
    """Test the database initialization script."""
    print("\nTesting database initialization script...")
    
    try:
        from mathematics_lab.database.init_db import create_initial_superadmin
        
        # This should create the superadmin if it doesn't exist
        create_initial_superadmin()
        print("✅ Database initialization script working")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization script error: {e}")
        return False


def main():
    """Run all Sprint 1 tests."""
    print("Mathematics Lab - Sprint 1 Testing")
    print("=" * 40)
    
    tests = [
        test_database_initialization,
        test_authentication,
        test_database_initialization_script
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Sprint 1 is working correctly!")
        print("\nYou can now run the application with:")
        print("python3 run.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)