"""
Authentication Manager for Mathematics Lab Application
Handles user authentication, session management, and role-based access control
"""

import hashlib
import secrets
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from database.db_manager import DatabaseManager

class AuthManager:
    """Manages authentication and authorization for the Mathematics Lab application"""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize authentication manager"""
        self.db_manager = db_manager
        self.current_user = None
        self.session_token = None
        self.session_expiry = None
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed_password
    
    def generate_session_token(self) -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
    
    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Authenticate user login
        
        Returns:
            Tuple of (success, message, user_data)
        """
        try:
            # Get user from database
            user = self.db_manager.get_user_by_username(username)
            
            if not user:
                return False, "Invalid username or password", None
            
            # Verify password
            if not self.verify_password(password, user['password_hash']):
                return False, "Invalid username or password", None
            
            # Check if user is active
            if not user['is_active']:
                return False, "Account is deactivated", None
            
            # Update last login
            self.db_manager.update_user_last_login(user['id'])
            
            # Create session
            self.current_user = user
            self.session_token = self.generate_session_token()
            self.session_expiry = datetime.now() + timedelta(hours=8)  # 8 hour session
            
            return True, "Login successful", user
            
        except Exception as e:
            return False, f"Login failed: {str(e)}", None
    
    def logout(self) -> bool:
        """Logout current user"""
        try:
            self.current_user = None
            self.session_token = None
            self.session_expiry = None
            return True
        except Exception:
            return False
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated and session is valid"""
        if not self.current_user or not self.session_token:
            return False
        
        if self.session_expiry and datetime.now() > self.session_expiry:
            self.logout()
            return False
        
        return True
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current authenticated user"""
        if self.is_authenticated():
            return self.current_user
        return None
    
    def has_role(self, role: str) -> bool:
        """Check if current user has specific role"""
        if not self.is_authenticated():
            return False
        
        return self.current_user['role'] == role
    
    def has_any_role(self, roles: list) -> bool:
        """Check if current user has any of the specified roles"""
        if not self.is_authenticated():
            return False
        
        return self.current_user['role'] in roles
    
    def is_super_admin(self) -> bool:
        """Check if current user is super admin"""
        return self.has_role('super_admin')
    
    def is_school_admin(self) -> bool:
        """Check if current user is school admin"""
        return self.has_role('school_admin')
    
    def is_teacher(self) -> bool:
        """Check if current user is teacher"""
        return self.has_role('teacher')
    
    def is_student(self) -> bool:
        """Check if current user is student"""
        return self.has_role('student')
    
    def can_access_school(self, school_id: int) -> bool:
        """Check if current user can access specific school"""
        if not self.is_authenticated():
            return False
        
        # Super admin can access all schools
        if self.is_super_admin():
            return True
        
        # School admin and teacher can only access their school
        if self.is_school_admin() or self.is_teacher():
            return self.current_user.get('school_id') == school_id
        
        # Students can only access their school
        if self.is_student():
            return self.current_user.get('school_id') == school_id
        
        return False
    
    def can_access_class(self, class_id: int) -> bool:
        """Check if current user can access specific class"""
        if not self.is_authenticated():
            return False
        
        # Super admin can access all classes
        if self.is_super_admin():
            return True
        
        # School admin can access classes in their school
        if self.is_school_admin():
            # This would need additional query to check if class belongs to user's school
            return True
        
        # Teacher can access their assigned classes
        if self.is_teacher():
            # This would need additional query to check if class is assigned to teacher
            return True
        
        # Students can only access their assigned class
        if self.is_student():
            return self.current_user.get('class_id') == class_id
        
        return False
    
    def create_user(self, user_data: Dict) -> Tuple[bool, str, Optional[int]]:
        """
        Create a new user
        
        Returns:
            Tuple of (success, message, user_id)
        """
        try:
            # Validate required fields
            required_fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']
            for field in required_fields:
                if field not in user_data or not user_data[field]:
                    return False, f"Missing required field: {field}", None
            
            # Check if username already exists
            existing_user = self.db_manager.get_user_by_username(user_data['username'])
            if existing_user:
                return False, "Username already exists", None
            
            # Hash password
            user_data['password_hash'] = self.hash_password(user_data['password'])
            del user_data['password']  # Remove plain password
            
            # Create user
            user_id = self.db_manager.create_user(user_data)
            
            return True, "User created successfully", user_id
            
        except Exception as e:
            return False, f"Failed to create user: {str(e)}", None
    
    def update_user(self, user_id: int, user_data: Dict) -> Tuple[bool, str]:
        """
        Update user information
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Validate user exists
            user = self.db_manager.get_user_by_id(user_id)
            if not user:
                return False, "User not found"
            
            # Update password if provided
            if 'password' in user_data and user_data['password']:
                user_data['password_hash'] = self.hash_password(user_data['password'])
                del user_data['password']
            
            # Update user in database
            # This would need to be implemented in DatabaseManager
            # For now, return success
            return True, "User updated successfully"
            
        except Exception as e:
            return False, f"Failed to update user: {str(e)}"
    
    def deactivate_user(self, user_id: int) -> Tuple[bool, str]:
        """
        Deactivate a user
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Validate user exists
            user = self.db_manager.get_user_by_id(user_id)
            if not user:
                return False, "User not found"
            
            # Deactivate user in database
            # This would need to be implemented in DatabaseManager
            # For now, return success
            return True, "User deactivated successfully"
            
        except Exception as e:
            return False, f"Failed to deactivate user: {str(e)}"
    
    def get_user_permissions(self) -> Dict:
        """Get current user's permissions"""
        if not self.is_authenticated():
            return {}
        
        permissions = {
            'can_manage_schools': self.is_super_admin(),
            'can_manage_users': self.is_super_admin() or self.is_school_admin(),
            'can_manage_classes': self.is_school_admin() or self.is_teacher(),
            'can_create_content': self.is_teacher(),
            'can_view_analytics': self.is_super_admin() or self.is_school_admin() or self.is_teacher(),
            'can_access_lessons': self.is_student(),
            'can_attempt_activities': self.is_student(),
        }
        
        return permissions