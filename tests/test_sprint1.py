"""
Unit tests for Sprint 1 - Database schema and authentication
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from auth.auth_manager import AuthManager

class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager"""
    
    def setUp(self):
        """Set up test database"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_mathlab.db")
        self.db_manager = DatabaseManager(self.db_path)
    
    def tearDown(self):
        """Clean up test database"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_create_tables(self):
        """Test database table creation"""
        try:
            self.db_manager.create_tables()
            # Check if tables exist by querying them
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            # Check users table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            self.assertIsNotNone(cursor.fetchone())
            
            # Check schools table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schools'")
            self.assertIsNotNone(cursor.fetchone())
            
            # Check classes table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='classes'")
            self.assertIsNotNone(cursor.fetchone())
            
            # Check topics table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='topics'")
            self.assertIsNotNone(cursor.fetchone())
            
            # Check lessons table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lessons'")
            self.assertIsNotNone(cursor.fetchone())
            
            # Check activities table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activities'")
            self.assertIsNotNone(cursor.fetchone())
            
            # Check student_attempts table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='student_attempts'")
            self.assertIsNotNone(cursor.fetchone())
            
            # Check student_progress table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='student_progress'")
            self.assertIsNotNone(cursor.fetchone())
            
            print("✅ Database table creation test passed")
            
        except Exception as e:
            self.fail(f"Database table creation failed: {e}")
    
    def test_create_sample_data(self):
        """Test sample data creation"""
        try:
            self.db_manager.create_tables()
            self.db_manager.create_sample_data()
            
            # Check if sample data was created
            schools = self.db_manager.get_schools()
            self.assertGreater(len(schools), 0)
            self.assertEqual(schools[0]['name'], "Delhi Public School")
            
            # Check if sample user was created
            user = self.db_manager.get_user_by_username("admin")
            self.assertIsNotNone(user)
            self.assertEqual(user['role'], "super_admin")
            
            # Check if topics were created
            topics_grade1 = self.db_manager.get_topics_by_grade(1)
            self.assertGreater(len(topics_grade1), 0)
            
            topics_grade6 = self.db_manager.get_topics_by_grade(6)
            self.assertGreater(len(topics_grade6), 0)
            
            topics_grade9 = self.db_manager.get_topics_by_grade(9)
            self.assertGreater(len(topics_grade9), 0)
            
            topics_grade12 = self.db_manager.get_topics_by_grade(12)
            self.assertGreater(len(topics_grade12), 0)
            
            print("✅ Sample data creation test passed")
            
        except Exception as e:
            self.fail(f"Sample data creation failed: {e}")
    
    def test_user_operations(self):
        """Test user operations"""
        try:
            self.db_manager.create_tables()
            
            # Test user creation
            user_data = {
                'username': 'testuser',
                'email': 'test@example.com',
                'password_hash': 'test_hash',
                'first_name': 'Test',
                'last_name': 'User',
                'role': 'teacher'
            }
            
            user_id = self.db_manager.create_user(user_data)
            self.assertIsNotNone(user_id)
            
            # Test user retrieval
            user = self.db_manager.get_user_by_username('testuser')
            self.assertIsNotNone(user)
            self.assertEqual(user['first_name'], 'Test')
            self.assertEqual(user['last_name'], 'User')
            self.assertEqual(user['role'], 'teacher')
            
            # Test user retrieval by ID
            user_by_id = self.db_manager.get_user_by_id(user_id)
            self.assertIsNotNone(user_by_id)
            self.assertEqual(user_by_id['username'], 'testuser')
            
            print("✅ User operations test passed")
            
        except Exception as e:
            self.fail(f"User operations failed: {e}")
    
    def test_school_operations(self):
        """Test school operations"""
        try:
            self.db_manager.create_tables()
            
            # Test school retrieval
            schools = self.db_manager.get_schools()
            self.assertIsInstance(schools, list)
            
            print("✅ School operations test passed")
            
        except Exception as e:
            self.fail(f"School operations failed: {e}")
    
    def test_topic_operations(self):
        """Test topic operations"""
        try:
            self.db_manager.create_tables()
            self.db_manager.create_sample_data()
            
            # Test topic retrieval by grade
            for grade in [1, 6, 9, 12]:
                topics = self.db_manager.get_topics_by_grade(grade)
                self.assertIsInstance(topics, list)
                self.assertGreater(len(topics), 0)
                
                # Verify topics are ordered correctly
                for i, topic in enumerate(topics):
                    self.assertEqual(topic['grade'], grade)
                    if i > 0:
                        self.assertGreaterEqual(topic['order_index'], topics[i-1]['order_index'])
            
            print("✅ Topic operations test passed")
            
        except Exception as e:
            self.fail(f"Topic operations failed: {e}")

class TestAuthManager(unittest.TestCase):
    """Test cases for AuthManager"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_mathlab.db")
        self.db_manager = DatabaseManager(self.db_path)
        self.auth_manager = AuthManager(self.db_manager)
        
        # Create test database
        self.db_manager.create_tables()
        self.db_manager.create_sample_data()
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        
        # Test password hashing
        hashed = self.auth_manager.hash_password(password)
        self.assertIsInstance(hashed, str)
        self.assertNotEqual(hashed, password)
        
        # Test password verification
        self.assertTrue(self.auth_manager.verify_password(password, hashed))
        self.assertFalse(self.auth_manager.verify_password("wrongpassword", hashed))
        
        print("✅ Password hashing test passed")
    
    def test_login_logout(self):
        """Test login and logout functionality"""
        # Test successful login
        success, message, user = self.auth_manager.login("admin", "admin123")
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "admin")
        self.assertEqual(user['role'], "super_admin")
        
        # Test authentication check
        self.assertTrue(self.auth_manager.is_authenticated())
        self.assertIsNotNone(self.auth_manager.get_current_user())
        
        # Test logout
        logout_success = self.auth_manager.logout()
        self.assertTrue(logout_success)
        self.assertFalse(self.auth_manager.is_authenticated())
        self.assertIsNone(self.auth_manager.get_current_user())
        
        print("✅ Login/logout test passed")
    
    def test_failed_login(self):
        """Test failed login attempts"""
        # Test wrong password
        success, message, user = self.auth_manager.login("admin", "wrongpassword")
        self.assertFalse(success)
        self.assertIsNone(user)
        
        # Test non-existent user
        success, message, user = self.auth_manager.login("nonexistent", "password")
        self.assertFalse(success)
        self.assertIsNone(user)
        
        print("✅ Failed login test passed")
    
    def test_role_checking(self):
        """Test role-based access control"""
        # Login as admin
        self.auth_manager.login("admin", "admin123")
        
        # Test role checking
        self.assertTrue(self.auth_manager.is_super_admin())
        self.assertFalse(self.auth_manager.is_school_admin())
        self.assertFalse(self.auth_manager.is_teacher())
        self.assertFalse(self.auth_manager.is_student())
        
        # Test has_role method
        self.assertTrue(self.auth_manager.has_role("super_admin"))
        self.assertFalse(self.auth_manager.has_role("teacher"))
        
        # Test has_any_role method
        self.assertTrue(self.auth_manager.has_any_role(["super_admin", "teacher"]))
        self.assertFalse(self.auth_manager.has_any_role(["teacher", "student"]))
        
        print("✅ Role checking test passed")
    
    def test_user_creation(self):
        """Test user creation functionality"""
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'teacher'
        }
        
        success, message, user_id = self.auth_manager.create_user(user_data)
        self.assertTrue(success)
        self.assertIsNotNone(user_id)
        
        # Test login with new user
        success, message, user = self.auth_manager.login("newuser", "newpassword123")
        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "newuser")
        self.assertEqual(user['role'], "teacher")
        
        print("✅ User creation test passed")
    
    def test_permissions(self):
        """Test user permissions"""
        # Login as admin
        self.auth_manager.login("admin", "admin123")
        
        permissions = self.auth_manager.get_user_permissions()
        self.assertIsInstance(permissions, dict)
        self.assertTrue(permissions['can_manage_schools'])
        self.assertTrue(permissions['can_manage_users'])
        self.assertTrue(permissions['can_view_analytics'])
        
        print("✅ Permissions test passed")

def run_sprint1_tests():
    """Run all Sprint 1 tests"""
    print("🧪 Running Sprint 1 Tests...")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add database tests
    test_suite.addTest(unittest.makeSuite(TestDatabaseManager))
    
    # Add authentication tests
    test_suite.addTest(unittest.makeSuite(TestAuthManager))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("=" * 50)
    if result.wasSuccessful():
        print("🎉 All Sprint 1 tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False

if __name__ == "__main__":
    run_sprint1_tests()