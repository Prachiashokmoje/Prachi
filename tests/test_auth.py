"""
Unit tests for authentication functionality
"""

import unittest
import tempfile
import os
from datetime import datetime, timedelta
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database.db_manager import DatabaseManager
from auth.auth_manager import AuthManager


class TestAuthManager(unittest.TestCase):
    """Test cases for AuthManager"""
    
    def setUp(self):
        """Set up test database and auth manager"""
        # Create temporary database for testing
        self.test_db_fd, self.test_db_path = tempfile.mkstemp()
        self.db = DatabaseManager(self.test_db_path)
        self.db.initialize_database()
        self.auth = AuthManager(self.db)
    
    def tearDown(self):
        """Clean up test database"""
        os.close(self.test_db_fd)
        os.unlink(self.test_db_path)
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        
        # Hash password
        hashed = self.auth.hash_password(password)
        self.assertIsInstance(hashed, str)
        self.assertNotEqual(password, hashed)
        
        # Verify correct password
        self.assertTrue(self.auth.verify_password(password, hashed))
        
        # Verify incorrect password
        self.assertFalse(self.auth.verify_password("wrongpassword", hashed))
    
    def test_create_user(self):
        """Test user creation"""
        # Create a user
        user_id = self.auth.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            role="Student",
            first_name="Test",
            last_name="User"
        )
        
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)
        
        # Verify user was created
        user = self.db.get_user_by_username("testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "testuser")
        self.assertEqual(user['email'], "test@example.com")
        self.assertEqual(user['role'], "Student")
        self.assertEqual(user['first_name'], "Test")
        self.assertEqual(user['last_name'], "User")
        
        # Verify password is hashed
        self.assertNotEqual(user['password_hash'], "password123")
        self.assertTrue(self.auth.verify_password("password123", user['password_hash']))
    
    def test_create_user_duplicate_username(self):
        """Test creating user with duplicate username"""
        # Create first user
        self.auth.create_user(
            username="testuser",
            email="test1@example.com",
            password="password123",
            role="Student"
        )
        
        # Try to create user with same username
        with self.assertRaises(ValueError) as context:
            self.auth.create_user(
                username="testuser",
                email="test2@example.com",
                password="password456",
                role="Teacher"
            )
        
        self.assertIn("Username already exists", str(context.exception))
    
    def test_create_user_duplicate_email(self):
        """Test creating user with duplicate email"""
        # Create first user
        self.auth.create_user(
            username="testuser1",
            email="test@example.com",
            password="password123",
            role="Student"
        )
        
        # Try to create user with same email
        with self.assertRaises(ValueError) as context:
            self.auth.create_user(
                username="testuser2",
                email="test@example.com",
                password="password456",
                role="Teacher"
            )
        
        self.assertIn("Email already exists", str(context.exception))
    
    def test_create_user_invalid_role(self):
        """Test creating user with invalid role"""
        with self.assertRaises(ValueError) as context:
            self.auth.create_user(
                username="testuser",
                email="test@example.com",
                password="password123",
                role="InvalidRole"
            )
        
        self.assertIn("Invalid role", str(context.exception))
    
    def test_authenticate_user(self):
        """Test user authentication"""
        # Create a user
        self.auth.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            role="Student",
            first_name="Test",
            last_name="User"
        )
        
        # Test successful authentication
        user = self.auth.authenticate_user("testuser", "password123")
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "testuser")
        self.assertEqual(user['email'], "test@example.com")
        self.assertEqual(user['role'], "Student")
        self.assertNotIn('password_hash', user)  # Should not include password hash
        
        # Test failed authentication - wrong password
        user = self.auth.authenticate_user("testuser", "wrongpassword")
        self.assertIsNone(user)
        
        # Test failed authentication - wrong username
        user = self.auth.authenticate_user("wronguser", "password123")
        self.assertIsNone(user)
    
    def test_session_management(self):
        """Test session creation and validation"""
        # Create a user
        user_id = self.auth.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            role="Student"
        )
        
        # Create session
        session_id = self.auth.create_session(user_id)
        self.assertIsInstance(session_id, str)
        self.assertGreater(len(session_id), 0)
        
        # Validate session
        session_data = self.auth.validate_session(session_id)
        self.assertIsNotNone(session_data)
        self.assertEqual(session_data['user_id'], user_id)
        self.assertEqual(session_data['username'], "testuser")
        
        # Invalidate session
        result = self.auth.invalidate_session(session_id)
        self.assertTrue(result)
        
        # Try to validate invalidated session
        session_data = self.auth.validate_session(session_id)
        self.assertIsNone(session_data)
    
    def test_change_password(self):
        """Test password change"""
        # Create a user
        user_id = self.auth.create_user(
            username="testuser",
            email="test@example.com",
            password="oldpassword",
            role="Student"
        )
        
        # Change password with correct old password
        result = self.auth.change_password(user_id, "oldpassword", "newpassword")
        self.assertTrue(result)
        
        # Verify old password no longer works
        user = self.auth.authenticate_user("testuser", "oldpassword")
        self.assertIsNone(user)
        
        # Verify new password works
        user = self.auth.authenticate_user("testuser", "newpassword")
        self.assertIsNotNone(user)
        
        # Try to change password with wrong old password
        result = self.auth.change_password(user_id, "wrongpassword", "newerpassword")
        self.assertFalse(result)
    
    def test_role_permissions(self):
        """Test role-based permissions"""
        # Test role hierarchy
        self.assertTrue(self.auth.check_role_permission("SuperAdmin", "Student"))
        self.assertTrue(self.auth.check_role_permission("SuperAdmin", "Teacher"))
        self.assertTrue(self.auth.check_role_permission("SuperAdmin", "SchoolAdmin"))
        self.assertTrue(self.auth.check_role_permission("SuperAdmin", "SuperAdmin"))
        
        self.assertTrue(self.auth.check_role_permission("SchoolAdmin", "Student"))
        self.assertTrue(self.auth.check_role_permission("SchoolAdmin", "Teacher"))
        self.assertTrue(self.auth.check_role_permission("SchoolAdmin", "SchoolAdmin"))
        self.assertFalse(self.auth.check_role_permission("SchoolAdmin", "SuperAdmin"))
        
        self.assertTrue(self.auth.check_role_permission("Teacher", "Student"))
        self.assertTrue(self.auth.check_role_permission("Teacher", "Teacher"))
        self.assertFalse(self.auth.check_role_permission("Teacher", "SchoolAdmin"))
        self.assertFalse(self.auth.check_role_permission("Teacher", "SuperAdmin"))
        
        self.assertTrue(self.auth.check_role_permission("Student", "Student"))
        self.assertFalse(self.auth.check_role_permission("Student", "Teacher"))
        self.assertFalse(self.auth.check_role_permission("Student", "SchoolAdmin"))
        self.assertFalse(self.auth.check_role_permission("Student", "SuperAdmin"))
    
    def test_school_access_permissions(self):
        """Test school access permissions"""
        # SuperAdmin can access any school
        self.assertTrue(self.auth.can_access_school("SuperAdmin", 1, 2))
        self.assertTrue(self.auth.can_access_school("SuperAdmin", None, 1))
        
        # Other roles can only access their own school
        self.assertTrue(self.auth.can_access_school("SchoolAdmin", 1, 1))
        self.assertFalse(self.auth.can_access_school("SchoolAdmin", 1, 2))
        
        self.assertTrue(self.auth.can_access_school("Teacher", 1, 1))
        self.assertFalse(self.auth.can_access_school("Teacher", 1, 2))
        
        self.assertTrue(self.auth.can_access_school("Student", 1, 1))
        self.assertFalse(self.auth.can_access_school("Student", 1, 2))
    
    def test_superadmin_existence(self):
        """Test superadmin existence check"""
        # Initially no superadmin
        self.assertFalse(self.auth.superadmin_exists())
        
        # Create a superadmin
        self.auth.create_user(
            username="admin",
            email="admin@example.com",
            password="password123",
            role="SuperAdmin"
        )
        
        # Now superadmin exists
        self.assertTrue(self.auth.superadmin_exists())
    
    def test_cleanup_expired_sessions(self):
        """Test cleanup of expired sessions"""
        # Create a user
        user_id = self.auth.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            role="Student"
        )
        
        # Create session manually with past expiry date
        expired_time = datetime.now() - timedelta(hours=1)
        query = '''
            INSERT INTO user_sessions (id, user_id, expires_at)
            VALUES (?, ?, ?)
        '''
        self.db.execute_insert(query, ("expired_session", user_id, expired_time))
        
        # Verify session exists
        query = "SELECT COUNT(*) as count FROM user_sessions WHERE id = ?"
        result = self.db.execute_query(query, ("expired_session",))
        self.assertEqual(result[0]['count'], 1)
        
        # Cleanup expired sessions
        cleaned_count = self.auth.cleanup_expired_sessions()
        self.assertGreater(cleaned_count, 0)
        
        # Verify expired session was removed
        result = self.db.execute_query(query, ("expired_session",))
        self.assertEqual(result[0]['count'], 0)
    
    def test_user_activation_deactivation(self):
        """Test user activation and deactivation"""
        # Create a user
        user_id = self.auth.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            role="Student"
        )
        
        # Verify user is active by default
        user = self.db.get_user_by_id(user_id)
        self.assertTrue(user['is_active'])
        
        # Deactivate user
        result = self.auth.deactivate_user(user_id)
        self.assertTrue(result)
        
        # Verify user is deactivated
        user = self.db.get_user_by_id(user_id)
        self.assertIsNone(user)  # get_user_by_id only returns active users
        
        # Verify authentication fails for deactivated user
        user = self.auth.authenticate_user("testuser", "password123")
        self.assertIsNone(user)
        
        # Reactivate user
        result = self.auth.activate_user(user_id)
        self.assertTrue(result)
        
        # Verify user is active again
        user = self.db.get_user_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertTrue(user['is_active'])


if __name__ == '__main__':
    unittest.main()