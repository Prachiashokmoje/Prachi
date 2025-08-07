"""
Unit tests for authentication module.
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from auth.authentication import AuthManager, AuthenticationError
from database.models import DatabaseManager


class TestAuthManager(unittest.TestCase):
    """Test cases for AuthManager class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Create database manager with temporary database
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.auth_manager = AuthManager()
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary database
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "TestPassword123!"
        hashed = self.auth_manager.hash_password(password)
        
        # Verify hash is different from original password
        self.assertNotEqual(password, hashed)
        
        # Verify password verification works
        self.assertTrue(self.auth_manager.verify_password(password, hashed))
        self.assertFalse(self.auth_manager.verify_password("WrongPassword", hashed))
    
    def test_password_validation(self):
        """Test password strength validation."""
        # Test valid password
        valid_password = "ValidPass123!"
        is_valid, message = self.auth_manager.validate_password(valid_password)
        self.assertTrue(is_valid)
        
        # Test too short password
        short_password = "Short1"
        is_valid, message = self.auth_manager.validate_password(short_password)
        self.assertFalse(is_valid)
        self.assertIn("at least", message)
        
        # Test password without uppercase
        no_upper = "validpass123!"
        is_valid, message = self.auth_manager.validate_password(no_upper)
        self.assertFalse(is_valid)
        self.assertIn("uppercase", message)
        
        # Test password without lowercase
        no_lower = "VALIDPASS123!"
        is_valid, message = self.auth_manager.validate_password(no_lower)
        self.assertFalse(is_valid)
        self.assertIn("lowercase", message)
        
        # Test password without digit
        no_digit = "ValidPassword!"
        is_valid, message = self.auth_manager.validate_password(no_digit)
        self.assertFalse(is_valid)
        self.assertIn("digit", message)
    
    def test_email_validation(self):
        """Test email format validation."""
        # Valid emails
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org"
        ]
        
        for email in valid_emails:
            self.assertTrue(self.auth_manager.validate_email(email))
        
        # Invalid emails
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "user@",
            "user@.com",
            "user..name@example.com"
        ]
        
        for email in invalid_emails:
            self.assertFalse(self.auth_manager.validate_email(email))
    
    def test_session_token_generation(self):
        """Test session token generation."""
        token1 = self.auth_manager.generate_session_token()
        token2 = self.auth_manager.generate_session_token()
        
        # Tokens should be different
        self.assertNotEqual(token1, token2)
        
        # Tokens should be strings
        self.assertIsInstance(token1, str)
        self.assertIsInstance(token2, str)
        
        # Tokens should have reasonable length
        self.assertGreater(len(token1), 20)
        self.assertGreater(len(token2), 20)
    
    def test_user_registration(self):
        """Test user registration."""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'ValidPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'student'
        }
        
        # Test successful registration
        user = self.auth_manager.register_user(**user_data)
        self.assertEqual(user['username'], user_data['username'])
        self.assertEqual(user['email'], user_data['email'])
        self.assertEqual(user['role'], user_data['role'])
        
        # Test duplicate username
        with self.assertRaises(AuthenticationError):
            self.auth_manager.register_user(**user_data)
        
        # Test duplicate email
        user_data['username'] = 'testuser2'
        with self.assertRaises(AuthenticationError):
            self.auth_manager.register_user(**user_data)
    
    def test_user_login(self):
        """Test user login."""
        # Register a user first
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'ValidPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'student'
        }
        
        self.auth_manager.register_user(**user_data)
        
        # Test successful login
        login_result = self.auth_manager.login('testuser', 'ValidPass123!')
        self.assertIn('session_token', login_result)
        self.assertIn('user', login_result)
        self.assertEqual(login_result['user']['username'], 'testuser')
        
        # Test wrong password
        with self.assertRaises(AuthenticationError):
            self.auth_manager.login('testuser', 'WrongPassword')
        
        # Test non-existent user
        with self.assertRaises(AuthenticationError):
            self.auth_manager.login('nonexistent', 'ValidPass123!')
    
    def test_role_based_access(self):
        """Test role-based access control."""
        # Register users with different roles
        users = [
            {
                'username': 'superadmin',
                'email': 'superadmin@example.com',
                'password': 'ValidPass123!',
                'first_name': 'Super',
                'last_name': 'Admin',
                'role': 'superadmin'
            },
            {
                'username': 'teacher',
                'email': 'teacher@example.com',
                'password': 'ValidPass123!',
                'first_name': 'Math',
                'last_name': 'Teacher',
                'role': 'teacher'
            },
            {
                'username': 'student',
                'email': 'student@example.com',
                'password': 'ValidPass123!',
                'first_name': 'John',
                'last_name': 'Student',
                'role': 'student'
            }
        ]
        
        for user_data in users:
            self.auth_manager.register_user(**user_data)
        
        # Login as superadmin
        superadmin_login = self.auth_manager.login('superadmin', 'ValidPass123!')
        superadmin_token = superadmin_login['session_token']
        
        # Test superadmin access
        user = self.auth_manager.require_superadmin(superadmin_token)
        self.assertEqual(user['role'], 'superadmin')
        
        # Test schooladmin access (superadmin should have access)
        user = self.auth_manager.require_schooladmin(superadmin_token)
        self.assertEqual(user['role'], 'superadmin')
        
        # Login as teacher
        teacher_login = self.auth_manager.login('teacher', 'ValidPass123!')
        teacher_token = teacher_login['session_token']
        
        # Test teacher access
        user = self.auth_manager.require_teacher(teacher_token)
        self.assertEqual(user['role'], 'teacher')
        
        # Test that teacher cannot access superadmin functions
        with self.assertRaises(AuthenticationError):
            self.auth_manager.require_superadmin(teacher_token)
        
        # Login as student
        student_login = self.auth_manager.login('student', 'ValidPass123!')
        student_token = student_login['session_token']
        
        # Test student access
        user = self.auth_manager.require_student(student_token)
        self.assertEqual(user['role'], 'student')
        
        # Test that student cannot access teacher functions
        with self.assertRaises(AuthenticationError):
            self.auth_manager.require_teacher(student_token)
    
    def test_session_management(self):
        """Test session management."""
        # Register and login user
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'ValidPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'student'
        }
        
        self.auth_manager.register_user(**user_data)
        login_result = self.auth_manager.login('testuser', 'ValidPass123!')
        session_token = login_result['session_token']
        
        # Test get current user
        user = self.auth_manager.get_current_user(session_token)
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], 'testuser')
        
        # Test logout
        self.assertTrue(self.auth_manager.logout(session_token))
        
        # Test that user cannot access after logout
        user = self.auth_manager.get_current_user(session_token)
        self.assertIsNone(user)


if __name__ == '__main__':
    unittest.main()