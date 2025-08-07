"""
Unit tests for database operations.
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from database.models import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Create database manager with temporary database
        self.db_manager = DatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary database
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_database_initialization(self):
        """Test database initialization creates all required tables."""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        # Check if all required tables exist
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
        
        self.assertEqual(set(tables), set(expected_tables))
        conn.close()
    
    def test_create_superadmin(self):
        """Test creating superadmin user."""
        user_data = {
            'username': 'testadmin',
            'email': 'admin@test.com',
            'password_hash': 'hashed_password',
            'first_name': 'Test',
            'last_name': 'Admin'
        }
        
        user_id = self.db_manager.create_superadmin(**user_data)
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)
        
        # Verify user was created
        user = self.db_manager.get_user_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], user_data['username'])
        self.assertEqual(user['role'], 'superadmin')
    
    def test_get_user_by_username(self):
        """Test getting user by username."""
        # Create a user first
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        user_id = self.db_manager.create_superadmin(**user_data)
        
        # Test getting user by username
        user = self.db_manager.get_user_by_username('testuser')
        self.assertIsNotNone(user)
        self.assertEqual(user['id'], user_id)
        self.assertEqual(user['username'], 'testuser')
        
        # Test getting non-existent user
        user = self.db_manager.get_user_by_username('nonexistent')
        self.assertIsNone(user)
    
    def test_get_user_by_id(self):
        """Test getting user by ID."""
        # Create a user first
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        user_id = self.db_manager.create_superadmin(**user_data)
        
        # Test getting user by ID
        user = self.db_manager.get_user_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user['id'], user_id)
        self.assertEqual(user['username'], 'testuser')
        
        # Test getting non-existent user
        user = self.db_manager.get_user_by_id(99999)
        self.assertIsNone(user)
    
    def test_session_management(self):
        """Test session creation, retrieval, and deletion."""
        # Create a user first
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        user_id = self.db_manager.create_superadmin(**user_data)
        
        # Test session creation
        session_token = "test_session_token"
        expires_at = datetime.now() + timedelta(hours=1)
        
        success = self.db_manager.create_session(user_id, session_token, expires_at)
        self.assertTrue(success)
        
        # Test getting session
        session = self.db_manager.get_session(session_token)
        self.assertIsNotNone(session)
        self.assertEqual(session['user_id'], user_id)
        self.assertEqual(session['session_token'], session_token)
        
        # Test deleting session
        deleted = self.db_manager.delete_session(session_token)
        self.assertTrue(deleted)
        
        # Verify session is deleted
        session = self.db_manager.get_session(session_token)
        self.assertIsNone(session)
    
    def test_session_expiration(self):
        """Test session expiration handling."""
        # Create a user first
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        user_id = self.db_manager.create_superadmin(**user_data)
        
        # Create expired session
        session_token = "expired_session_token"
        expires_at = datetime.now() - timedelta(hours=1)  # Expired 1 hour ago
        
        success = self.db_manager.create_session(user_id, session_token, expires_at)
        self.assertTrue(success)
        
        # Test that expired session is not returned
        session = self.db_manager.get_session(session_token)
        self.assertIsNone(session)
    
    def test_cleanup_expired_sessions(self):
        """Test cleanup of expired sessions."""
        # Create a user first
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        user_id = self.db_manager.create_superadmin(**user_data)
        
        # Create both valid and expired sessions
        valid_token = "valid_session_token"
        expired_token = "expired_session_token"
        
        valid_expires = datetime.now() + timedelta(hours=1)
        expired_expires = datetime.now() - timedelta(hours=1)
        
        self.db_manager.create_session(user_id, valid_token, valid_expires)
        self.db_manager.create_session(user_id, expired_token, expired_expires)
        
        # Verify both sessions exist
        self.assertIsNotNone(self.db_manager.get_session(valid_token))
        self.assertIsNone(self.db_manager.get_session(expired_token))  # Already filtered out
        
        # Run cleanup
        self.db_manager.cleanup_expired_sessions()
        
        # Verify valid session still exists
        self.assertIsNotNone(self.db_manager.get_session(valid_token))
    
    def test_database_connection(self):
        """Test database connection functionality."""
        conn = self.db_manager.get_connection()
        self.assertIsNotNone(conn)
        
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        self.assertEqual(result[0], 1)
        
        conn.close()
    
    def test_user_activation_status(self):
        """Test user activation status handling."""
        # Create an active user
        user_data = {
            'username': 'activeuser',
            'email': 'active@example.com',
            'password_hash': 'hashed_password',
            'first_name': 'Active',
            'last_name': 'User'
        }
        
        user_id = self.db_manager.create_superadmin(**user_data)
        
        # Verify user is active by default
        user = self.db_manager.get_user_by_username('activeuser')
        self.assertTrue(user['is_active'])
        
        # Deactivate user
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_active = 0 WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        # Verify deactivated user is not returned
        user = self.db_manager.get_user_by_username('activeuser')
        self.assertIsNone(user)


if __name__ == '__main__':
    unittest.main()