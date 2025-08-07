"""
Unit tests for database operations
"""

import unittest
import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database.db_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager"""
    
    def setUp(self):
        """Set up test database"""
        # Create temporary database for testing
        self.test_db_fd, self.test_db_path = tempfile.mkstemp()
        self.db = DatabaseManager(self.test_db_path)
        self.db.initialize_database()
    
    def tearDown(self):
        """Clean up test database"""
        self.db.close_connection()
        os.close(self.test_db_fd)
        os.unlink(self.test_db_path)
    
    def test_database_initialization(self):
        """Test database initialization creates all required tables"""
        # Get list of tables
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        tables = self.db.execute_query(query)
        table_names = [table['name'] for table in tables]
        
        # Check that all required tables exist
        required_tables = [
            'users', 'schools', 'classes', 'teacher_classes', 'student_enrollments',
            'cbse_topics', 'lessons', 'activities', 'activity_attempts',
            'student_progress', 'user_sessions', 'app_settings'
        ]
        
        for table in required_tables:
            self.assertIn(table, table_names, f"Table {table} not found")
    
    def test_create_and_get_user(self):
        """Test user creation and retrieval"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'role': 'Student',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        # Create user
        user_id = self.db.create_user(user_data)
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)
        
        # Get user by username
        user = self.db.get_user_by_username('testuser')
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], 'testuser')
        self.assertEqual(user['email'], 'test@example.com')
        self.assertEqual(user['role'], 'Student')
        self.assertEqual(user['first_name'], 'Test')
        self.assertEqual(user['last_name'], 'User')
        self.assertTrue(user['is_active'])
        
        # Get user by ID
        user_by_id = self.db.get_user_by_id(user_id)
        self.assertIsNotNone(user_by_id)
        self.assertEqual(user_by_id['id'], user_id)
        self.assertEqual(user_by_id['username'], 'testuser')
    
    def test_update_user(self):
        """Test user update"""
        # Create user
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'role': 'Student'
        }
        user_id = self.db.create_user(user_data)
        
        # Update user
        update_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com'
        }
        rows_affected = self.db.update_user(user_id, update_data)
        self.assertEqual(rows_affected, 1)
        
        # Verify update
        user = self.db.get_user_by_id(user_id)
        self.assertEqual(user['first_name'], 'Updated')
        self.assertEqual(user['last_name'], 'User')
        self.assertEqual(user['email'], 'updated@example.com')
    
    def test_create_and_get_school(self):
        """Test school creation and retrieval"""
        school_data = {
            'name': 'Test School',
            'address': '123 Test Street',
            'contact_email': 'school@test.com',
            'contact_phone': '555-0123'
        }
        
        # Create school
        school_id = self.db.create_school(school_data)
        self.assertIsInstance(school_id, int)
        self.assertGreater(school_id, 0)
        
        # Get school by ID
        school = self.db.get_school_by_id(school_id)
        self.assertIsNotNone(school)
        self.assertEqual(school['name'], 'Test School')
        self.assertEqual(school['address'], '123 Test Street')
        self.assertEqual(school['contact_email'], 'school@test.com')
        self.assertEqual(school['contact_phone'], '555-0123')
        self.assertTrue(school['is_active'])
        
        # Get all schools
        schools = self.db.get_schools()
        self.assertGreater(len(schools), 0)
        school_ids = [school['id'] for school in schools]
        self.assertIn(school_id, school_ids)
    
    def test_user_uniqueness_constraints(self):
        """Test that username and email uniqueness is enforced"""
        user_data1 = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'role': 'Student'
        }
        
        # Create first user
        user_id1 = self.db.create_user(user_data1)
        self.assertIsInstance(user_id1, int)
        
        # Try to create user with same username
        user_data2 = {
            'username': 'testuser',  # Same username
            'email': 'different@example.com',
            'password_hash': 'hashed_password',
            'role': 'Teacher'
        }
        
        with self.assertRaises(Exception):  # Should raise integrity error
            self.db.create_user(user_data2)
        
        # Try to create user with same email
        user_data3 = {
            'username': 'different_user',
            'email': 'test@example.com',  # Same email
            'password_hash': 'hashed_password',
            'role': 'Teacher'
        }
        
        with self.assertRaises(Exception):  # Should raise integrity error
            self.db.create_user(user_data3)
    
    def test_execute_query_methods(self):
        """Test the generic execute methods"""
        # Test execute_insert
        query = "INSERT INTO app_settings (setting_key, setting_value) VALUES (?, ?)"
        setting_id = self.db.execute_insert(query, ('test_key', 'test_value'))
        self.assertIsInstance(setting_id, int)
        self.assertGreater(setting_id, 0)
        
        # Test execute_query
        query = "SELECT * FROM app_settings WHERE setting_key = ?"
        results = self.db.execute_query(query, ('test_key',))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['setting_key'], 'test_key')
        self.assertEqual(results[0]['setting_value'], 'test_value')
        
        # Test execute_update
        query = "UPDATE app_settings SET setting_value = ? WHERE setting_key = ?"
        rows_affected = self.db.execute_update(query, ('updated_value', 'test_key'))
        self.assertEqual(rows_affected, 1)
        
        # Verify update
        query = "SELECT setting_value FROM app_settings WHERE setting_key = ?"
        results = self.db.execute_query(query, ('test_key',))
        self.assertEqual(results[0]['setting_value'], 'updated_value')
    
    def test_role_constraints(self):
        """Test that role constraints are enforced"""
        # Valid roles should work
        valid_roles = ['SuperAdmin', 'SchoolAdmin', 'Teacher', 'Student']
        
        for i, role in enumerate(valid_roles):
            user_data = {
                'username': f'user{i}',
                'email': f'user{i}@example.com',
                'password_hash': 'hashed_password',
                'role': role
            }
            user_id = self.db.create_user(user_data)
            self.assertIsInstance(user_id, int)
        
        # Invalid role should fail
        invalid_user_data = {
            'username': 'invaliduser',
            'email': 'invalid@example.com',
            'password_hash': 'hashed_password',
            'role': 'InvalidRole'
        }
        
        with self.assertRaises(Exception):  # Should raise constraint error
            self.db.create_user(invalid_user_data)
    
    def test_foreign_key_relationships(self):
        """Test foreign key relationships"""
        # Create a school first
        school_data = {
            'name': 'Test School',
            'address': '123 Test Street'
        }
        school_id = self.db.create_school(school_data)
        
        # Create a user with school_id
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'role': 'Student',
            'school_id': school_id
        }
        user_id = self.db.create_user(user_data)
        
        # Verify the relationship
        user = self.db.get_user_by_id(user_id)
        self.assertEqual(user['school_id'], school_id)
        
        school = self.db.get_school_by_id(school_id)
        self.assertIsNotNone(school)
    
    def test_indexes_creation(self):
        """Test that indexes are created"""
        # This is a basic test to ensure indexes don't cause errors
        # In a real scenario, you might want to check the EXPLAIN QUERY PLAN
        
        # Create some test data
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'role': 'Student'
        }
        user_id = self.db.create_user(user_data)
        
        # Queries that should use indexes
        queries = [
            ("SELECT * FROM users WHERE role = ?", ('Student',)),
            ("SELECT * FROM users WHERE school_id = ?", (1,)),
        ]
        
        for query, params in queries:
            # These should execute without error and potentially benefit from indexes
            results = self.db.execute_query(query, params)
            # Just verify the query executes successfully
            self.assertIsInstance(results, list)
    
    def test_connection_management(self):
        """Test database connection management"""
        # Test getting connection
        conn = self.db.get_connection()
        self.assertIsNotNone(conn)
        
        # Test that the same connection is returned
        conn2 = self.db.get_connection()
        self.assertEqual(conn, conn2)
        
        # Test closing connection
        self.db.close_connection()
        
        # Test that a new connection is created after closing
        conn3 = self.db.get_connection()
        self.assertIsNotNone(conn3)
    
    def test_empty_queries(self):
        """Test behavior with empty result sets"""
        # Query for non-existent user
        user = self.db.get_user_by_username('nonexistent')
        self.assertIsNone(user)
        
        user = self.db.get_user_by_id(99999)
        self.assertIsNone(user)
        
        # Query for non-existent school
        school = self.db.get_school_by_id(99999)
        self.assertIsNone(school)
        
        # When no schools exist
        schools = self.db.get_schools()
        self.assertEqual(len(schools), 0)


if __name__ == '__main__':
    unittest.main()