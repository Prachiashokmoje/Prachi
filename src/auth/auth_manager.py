"""
Authentication Manager for Mathematics Lab Application
Handles user authentication, password hashing, and session management
"""

import bcrypt
import secrets
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from database.db_manager import DatabaseManager


class AuthManager:
    """Manages user authentication and sessions"""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize authentication manager"""
        self.db = db_manager
        self.session_duration_hours = 24  # Default session duration
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user with username and password"""
        user = self.db.get_user_by_username(username)
        if not user:
            return None
        
        if not self.verify_password(password, user['password_hash']):
            return None
        
        # Return user data without password hash
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'school_id': user['school_id'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'is_active': user['is_active']
        }
    
    def create_session(self, user_id: int) -> str:
        """Create a new session for a user"""
        session_id = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(hours=self.session_duration_hours)
        
        # Clean up expired sessions for this user
        self.cleanup_expired_sessions(user_id)
        
        # Create new session
        query = '''
            INSERT INTO user_sessions (id, user_id, expires_at)
            VALUES (?, ?, ?)
        '''
        self.db.execute_insert(query, (session_id, user_id, expires_at))
        
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Validate a session and return user data if valid"""
        if not session_id:
            return None
        
        query = '''
            SELECT s.*, u.id as user_id, u.username, u.email, u.role, 
                   u.school_id, u.first_name, u.last_name, u.is_active
            FROM user_sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.id = ? AND s.is_active = 1 AND s.expires_at > ? AND u.is_active = 1
        '''
        
        results = self.db.execute_query(query, (session_id, datetime.now()))
        
        if not results:
            return None
        
        session = results[0]
        return {
            'session_id': session['id'],
            'user_id': session['user_id'],
            'username': session['username'],
            'email': session['email'],
            'role': session['role'],
            'school_id': session['school_id'],
            'first_name': session['first_name'],
            'last_name': session['last_name'],
            'is_active': session['is_active']
        }
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate a session"""
        query = "UPDATE user_sessions SET is_active = 0 WHERE id = ?"
        rows_affected = self.db.execute_update(query, (session_id,))
        return rows_affected > 0
    
    def cleanup_expired_sessions(self, user_id: int = None) -> int:
        """Clean up expired sessions"""
        if user_id:
            query = "DELETE FROM user_sessions WHERE user_id = ? AND expires_at <= ?"
            params = (user_id, datetime.now())
        else:
            query = "DELETE FROM user_sessions WHERE expires_at <= ?"
            params = (datetime.now(),)
        
        return self.db.execute_update(query, params)
    
    def create_user(self, username: str, email: str, password: str, role: str, 
                   school_id: int = None, first_name: str = None, 
                   last_name: str = None) -> int:
        """Create a new user with hashed password"""
        
        # Validate role
        valid_roles = ['SuperAdmin', 'SchoolAdmin', 'Teacher', 'Student']
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {valid_roles}")
        
        # Check if username already exists
        existing_user = self.db.get_user_by_username(username)
        if existing_user:
            raise ValueError("Username already exists")
        
        # Check if email already exists
        query = "SELECT id FROM users WHERE email = ?"
        existing_email = self.db.execute_query(query, (email,))
        if existing_email:
            raise ValueError("Email already exists")
        
        # Hash password
        password_hash = self.hash_password(password)
        
        # Create user data
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'role': role,
            'school_id': school_id,
            'first_name': first_name,
            'last_name': last_name
        }
        
        return self.db.create_user(user_data)
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password"""
        user = self.db.get_user_by_id(user_id)
        if not user:
            return False
        
        # Verify old password
        if not self.verify_password(old_password, user['password_hash']):
            return False
        
        # Hash new password
        new_password_hash = self.hash_password(new_password)
        
        # Update password
        user_data = {'password_hash': new_password_hash}
        rows_affected = self.db.update_user(user_id, user_data)
        
        return rows_affected > 0
    
    def reset_password(self, user_id: int, new_password: str) -> bool:
        """Reset user password (admin function)"""
        # Hash new password
        new_password_hash = self.hash_password(new_password)
        
        # Update password
        user_data = {'password_hash': new_password_hash}
        rows_affected = self.db.update_user(user_id, user_data)
        
        return rows_affected > 0
    
    def check_role_permission(self, user_role: str, required_role: str) -> bool:
        """Check if user role has permission for required role"""
        role_hierarchy = {
            'SuperAdmin': 4,
            'SchoolAdmin': 3,
            'Teacher': 2,
            'Student': 1
        }
        
        user_level = role_hierarchy.get(user_role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level
    
    def can_access_school(self, user_role: str, user_school_id: int, 
                         target_school_id: int) -> bool:
        """Check if user can access a specific school"""
        if user_role == 'SuperAdmin':
            return True
        
        if user_role in ['SchoolAdmin', 'Teacher', 'Student']:
            return user_school_id == target_school_id
        
        return False
    
    def superadmin_exists(self) -> bool:
        """Check if any SuperAdmin exists in the system"""
        query = "SELECT COUNT(*) as count FROM users WHERE role = 'SuperAdmin' AND is_active = 1"
        result = self.db.execute_query(query)
        return result[0]['count'] > 0
    
    def create_default_superadmin(self) -> int:
        """Create default SuperAdmin account"""
        return self.create_user(
            username='admin',
            email='admin@mathlab.com',
            password='admin123',
            role='SuperAdmin',
            first_name='System',
            last_name='Administrator'
        )
    
    def get_users_by_role(self, role: str, school_id: int = None) -> List[Dict[str, Any]]:
        """Get users by role and optionally by school"""
        if school_id:
            query = '''
                SELECT id, username, email, role, school_id, first_name, last_name, 
                       is_active, created_at
                FROM users 
                WHERE role = ? AND school_id = ? AND is_active = 1
                ORDER BY first_name, last_name
            '''
            params = (role, school_id)
        else:
            query = '''
                SELECT id, username, email, role, school_id, first_name, last_name, 
                       is_active, created_at
                FROM users 
                WHERE role = ? AND is_active = 1
                ORDER BY first_name, last_name
            '''
            params = (role,)
        
        results = self.db.execute_query(query, params)
        return [dict(row) for row in results]
    
    def get_school_users(self, school_id: int) -> List[Dict[str, Any]]:
        """Get all users for a specific school"""
        query = '''
            SELECT id, username, email, role, school_id, first_name, last_name, 
                   is_active, created_at
            FROM users 
            WHERE school_id = ? AND is_active = 1
            ORDER BY role, first_name, last_name
        '''
        
        results = self.db.execute_query(query, (school_id,))
        return [dict(row) for row in results]
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user account"""
        user_data = {'is_active': False}
        rows_affected = self.db.update_user(user_id, user_data)
        
        # Invalidate all sessions for this user
        query = "UPDATE user_sessions SET is_active = 0 WHERE user_id = ?"
        self.db.execute_update(query, (user_id,))
        
        return rows_affected > 0
    
    def activate_user(self, user_id: int) -> bool:
        """Activate a user account"""
        user_data = {'is_active': True}
        rows_affected = self.db.update_user(user_id, user_data)
        return rows_affected > 0