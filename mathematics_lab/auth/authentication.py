"""
Authentication module for Mathematics Lab application.
Handles user authentication, password hashing, and role-based access control.
"""

import bcrypt
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
import re

from ..database.models import db_manager


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass


class AuthManager:
    """Manages user authentication and authorization."""
    
    def __init__(self):
        self.password_min_length = 8
        self.session_duration = timedelta(hours=24)
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """Validate password strength."""
        if len(password) < self.password_min_length:
            return False, f"Password must be at least {self.password_min_length} characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        
        return True, "Password is valid"
    
    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def generate_session_token(self) -> str:
        """Generate a secure session token."""
        return secrets.token_urlsafe(32)
    
    def register_user(self, username: str, email: str, password: str, 
                     first_name: str, last_name: str, role: str, 
                     school_id: Optional[int] = None) -> Dict[str, Any]:
        """Register a new user."""
        # Validate inputs
        if not username or not email or not password:
            raise AuthenticationError("All fields are required")
        
        if not self.validate_email(email):
            raise AuthenticationError("Invalid email format")
        
        is_valid, message = self.validate_password(password)
        if not is_valid:
            raise AuthenticationError(message)
        
        # Check if username or email already exists
        existing_user = db_manager.get_user_by_username(username)
        if existing_user:
            raise AuthenticationError("Username already exists")
        
        # Hash password
        password_hash = self.hash_password(password)
        
        # Create user
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role, first_name, last_name, school_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, role, first_name, last_name, school_id))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            return {
                'id': user_id,
                'username': username,
                'email': email,
                'role': role,
                'first_name': first_name,
                'last_name': last_name,
                'school_id': school_id
            }
        except sqlite3.IntegrityError as e:
            conn.rollback()
            if "UNIQUE constraint failed" in str(e):
                if "email" in str(e):
                    raise AuthenticationError("Email already exists")
                else:
                    raise AuthenticationError("Username already exists")
            raise AuthenticationError("Registration failed")
        finally:
            conn.close()
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user and create session."""
        if not username or not password:
            raise AuthenticationError("Username and password are required")
        
        # Get user
        user = db_manager.get_user_by_username(username)
        if not user:
            raise AuthenticationError("Invalid username or password")
        
        # Verify password
        if not self.verify_password(password, user['password_hash']):
            raise AuthenticationError("Invalid username or password")
        
        # Check if user is active
        if not user['is_active']:
            raise AuthenticationError("Account is deactivated")
        
        # Create session
        session_token = self.generate_session_token()
        expires_at = datetime.now() + self.session_duration
        
        if not db_manager.create_session(user['id'], session_token, expires_at):
            raise AuthenticationError("Failed to create session")
        
        return {
            'session_token': session_token,
            'expires_at': expires_at.isoformat(),
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'school_id': user['school_id']
            }
        }
    
    def logout(self, session_token: str) -> bool:
        """Logout user by deleting session."""
        return db_manager.delete_session(session_token)
    
    def get_current_user(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Get current user from session token."""
        session = db_manager.get_session(session_token)
        if not session:
            return None
        
        return {
            'id': session['user_id'],
            'username': session['username'],
            'email': session['email'],
            'role': session['role'],
            'first_name': session['first_name'],
            'last_name': session['last_name'],
            'school_id': session['school_id']
        }
    
    def require_auth(self, session_token: str) -> Dict[str, Any]:
        """Require authentication and return user or raise error."""
        user = self.get_current_user(session_token)
        if not user:
            raise AuthenticationError("Authentication required")
        return user
    
    def require_role(self, session_token: str, required_roles: list) -> Dict[str, Any]:
        """Require specific role(s) and return user or raise error."""
        user = self.require_auth(session_token)
        if user['role'] not in required_roles:
            raise AuthenticationError("Insufficient permissions")
        return user
    
    def require_superadmin(self, session_token: str) -> Dict[str, Any]:
        """Require superadmin role."""
        return self.require_role(session_token, ['superadmin'])
    
    def require_schooladmin(self, session_token: str) -> Dict[str, Any]:
        """Require schooladmin role."""
        return self.require_role(session_token, ['superadmin', 'schooladmin'])
    
    def require_teacher(self, session_token: str) -> Dict[str, Any]:
        """Require teacher role."""
        return self.require_role(session_token, ['superadmin', 'schooladmin', 'teacher'])
    
    def require_student(self, session_token: str) -> Dict[str, Any]:
        """Require student role."""
        return self.require_role(session_token, ['superadmin', 'schooladmin', 'teacher', 'student'])
    
    def create_school(self, session_token: str, name: str, address: str = None,
                     contact_email: str = None, contact_phone: str = None) -> Dict[str, Any]:
        """Create a new school (SuperAdmin only)."""
        user = self.require_superadmin(session_token)
        
        if not name:
            raise AuthenticationError("School name is required")
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO schools (name, address, contact_email, contact_phone)
                VALUES (?, ?, ?, ?)
            ''', (name, address, contact_email, contact_phone))
            
            school_id = cursor.lastrowid
            conn.commit()
            
            return {
                'id': school_id,
                'name': name,
                'address': address,
                'contact_email': contact_email,
                'contact_phone': contact_phone
            }
        except sqlite3.IntegrityError:
            conn.rollback()
            raise AuthenticationError("Failed to create school")
        finally:
            conn.close()
    
    def get_schools(self, session_token: str) -> list:
        """Get all schools (SuperAdmin only)."""
        user = self.require_superadmin(session_token)
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM schools WHERE is_active = 1')
        schools = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return schools
    
    def get_school_users(self, session_token: str, school_id: int) -> list:
        """Get users for a specific school."""
        user = self.require_schooladmin(session_token)
        
        # Check if user has access to this school
        if user['role'] == 'schooladmin' and user['school_id'] != school_id:
            raise AuthenticationError("Access denied to this school")
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE school_id = ? AND is_active = 1
            ORDER BY role, first_name, last_name
        ''', (school_id,))
        
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users


# Global authentication manager instance
auth_manager = AuthManager()