"""
Session management for Mathematics Lab application.
Handles session tokens, validation, and cleanup.
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from ..database.models import db_manager
from .authentication import auth_manager


class SessionManager:
    """Manages user sessions and token validation."""
    
    def __init__(self):
        self.cleanup_interval = 3600  # 1 hour
        self.cleanup_thread = None
        self.running = False
    
    def start_cleanup_thread(self):
        """Start the background cleanup thread."""
        if self.cleanup_thread is None or not self.cleanup_thread.is_alive():
            self.running = True
            self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
            self.cleanup_thread.start()
    
    def stop_cleanup_thread(self):
        """Stop the background cleanup thread."""
        self.running = False
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            self.cleanup_thread.join(timeout=5)
    
    def _cleanup_loop(self):
        """Background loop for cleaning up expired sessions."""
        while self.running:
            try:
                db_manager.cleanup_expired_sessions()
                time.sleep(self.cleanup_interval)
            except Exception as e:
                print(f"Session cleanup error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def validate_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Validate session token and return user info."""
        if not session_token:
            return None
        
        return auth_manager.get_current_user(session_token)
    
    def refresh_session(self, session_token: str) -> Optional[str]:
        """Refresh session token and return new token."""
        user = self.validate_session(session_token)
        if not user:
            return None
        
        # Delete old session
        db_manager.delete_session(session_token)
        
        # Create new session
        new_token = auth_manager.generate_session_token()
        expires_at = datetime.now() + auth_manager.session_duration
        
        if db_manager.create_session(user['id'], new_token, expires_at):
            return new_token
        
        return None
    
    def get_session_info(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Get detailed session information."""
        session = db_manager.get_session(session_token)
        if not session:
            return None
        
        return {
            'user_id': session['user_id'],
            'username': session['username'],
            'role': session['role'],
            'expires_at': session['expires_at'],
            'created_at': session['created_at']
        }
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions."""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM sessions WHERE expires_at > datetime("now")')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def get_user_sessions(self, user_id: int) -> list:
        """Get all active sessions for a user."""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM sessions 
            WHERE user_id = ? AND expires_at > datetime('now')
            ORDER BY created_at DESC
        ''', (user_id,))
        
        sessions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return sessions
    
    def revoke_user_sessions(self, user_id: int) -> bool:
        """Revoke all sessions for a user."""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sessions WHERE user_id = ?', (user_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        return deleted
    
    def revoke_session(self, session_token: str) -> bool:
        """Revoke a specific session."""
        return db_manager.delete_session(session_token)


# Global session manager instance
session_manager = SessionManager()