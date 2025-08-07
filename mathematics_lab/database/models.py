"""
Database models for Mathematics Lab application.
Defines all tables and their relationships.
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, db_path: str = "mathematics_lab.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize the database with all tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('superadmin', 'schooladmin', 'teacher', 'student')),
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                school_id INTEGER,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_id) REFERENCES schools (id)
            )
        ''')
        
        # Schools table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                contact_email TEXT,
                contact_phone TEXT,
                admin_id INTEGER,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (admin_id) REFERENCES users (id)
            )
        ''')
        
        # Classes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_id INTEGER NOT NULL,
                grade INTEGER NOT NULL CHECK (grade >= 1 AND grade <= 12),
                section TEXT,
                teacher_id INTEGER,
                academic_year TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_id) REFERENCES schools (id),
                FOREIGN KEY (teacher_id) REFERENCES users (id)
            )
        ''')
        
        # Topics table (CBSE syllabus)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grade INTEGER NOT NULL CHECK (grade >= 1 AND grade <= 12),
                chapter_name TEXT NOT NULL,
                topic_name TEXT NOT NULL,
                description TEXT,
                objectives TEXT,
                prerequisites TEXT,
                content_json TEXT,
                difficulty_level TEXT CHECK (difficulty_level IN ('easy', 'medium', 'hard')),
                estimated_hours INTEGER DEFAULT 1,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Lessons table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                examples TEXT,
                teacher_notes TEXT,
                created_by INTEGER NOT NULL,
                is_published BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Activities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER NOT NULL,
                lesson_id INTEGER,
                title TEXT NOT NULL,
                activity_type TEXT NOT NULL CHECK (activity_type IN ('mcq', 'fill_blank', 'short_answer', 'step_by_step', 'simulation')),
                content_json TEXT NOT NULL,
                difficulty_level TEXT CHECK (difficulty_level IN ('easy', 'medium', 'hard')),
                max_score INTEGER DEFAULT 10,
                time_limit INTEGER,
                created_by INTEGER NOT NULL,
                is_published BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics (id),
                FOREIGN KEY (lesson_id) REFERENCES lessons (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Student Activity Attempts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                activity_id INTEGER NOT NULL,
                answers_json TEXT,
                score INTEGER,
                max_score INTEGER,
                time_spent INTEGER,
                is_completed BOOLEAN DEFAULT 0,
                feedback TEXT,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (id),
                FOREIGN KEY (activity_id) REFERENCES activities (id)
            )
        ''')
        
        # Student Progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                topic_id INTEGER NOT NULL,
                progress_percentage REAL DEFAULT 0,
                total_activities INTEGER DEFAULT 0,
                completed_activities INTEGER DEFAULT 0,
                average_score REAL DEFAULT 0,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (id),
                FOREIGN KEY (topic_id) REFERENCES topics (id),
                UNIQUE(student_id, topic_id)
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_topics_grade ON topics(grade)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_activities_topic ON activities(topic_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attempts_student ON activity_attempts(student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(session_token)')
        
        conn.commit()
        conn.close()
    
    def create_superadmin(self, username: str, email: str, password_hash: str, 
                         first_name: str, last_name: str) -> int:
        """Create the initial superadmin user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role, first_name, last_name)
                VALUES (?, ?, ?, 'superadmin', ?, ?)
            ''', (username, email, password_hash, first_name, last_name))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', (username,))
        user = cursor.fetchone()
        
        conn.close()
        return dict(user) if user else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ? AND is_active = 1', (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        return dict(user) if user else None
    
    def create_session(self, user_id: int, session_token: str, expires_at: datetime) -> bool:
        """Create a new session."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO sessions (user_id, session_token, expires_at)
                VALUES (?, ?, ?)
            ''', (user_id, session_token, expires_at))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Get session by token."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.*, u.* FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_token = ? AND s.expires_at > datetime('now')
        ''', (session_token,))
        
        session = cursor.fetchone()
        conn.close()
        
        return dict(session) if session else None
    
    def delete_session(self, session_token: str) -> bool:
        """Delete a session."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sessions WHERE session_token = ?', (session_token,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        return deleted
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sessions WHERE expires_at <= datetime("now")')
        conn.commit()
        conn.close()


# Global database manager instance
db_manager = DatabaseManager()