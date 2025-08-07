"""
Database Manager for Mathematics Lab Application
Handles SQLite database operations and schema management
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class DatabaseManager:
    """Manages SQLite database operations and schema"""
    
    def __init__(self, db_path: str = None):
        """Initialize database manager"""
        if db_path is None:
            # Create data directory if it doesn't exist
            data_dir = Path(__file__).parent.parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            self.db_path = str(data_dir / "mathlab.db")
        else:
            self.db_path = db_path
        
        self.connection = None
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self):
        """Initialize database with all required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL CHECK(role IN ('SuperAdmin', 'SchoolAdmin', 'Teacher', 'Student')),
                school_id INTEGER,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
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
                name VARCHAR(200) NOT NULL,
                address TEXT,
                contact_email VARCHAR(100),
                contact_phone VARCHAR(20),
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
                grade INTEGER NOT NULL CHECK(grade >= 1 AND grade <= 12),
                section VARCHAR(10),
                name VARCHAR(100),
                academic_year VARCHAR(10),
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_id) REFERENCES schools (id)
            )
        ''')
        
        # Teacher-Class assignments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teacher_classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER NOT NULL,
                class_id INTEGER NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES users (id),
                FOREIGN KEY (class_id) REFERENCES classes (id),
                UNIQUE(teacher_id, class_id)
            )
        ''')
        
        # Student-Class enrollments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                class_id INTEGER NOT NULL,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES users (id),
                FOREIGN KEY (class_id) REFERENCES classes (id),
                UNIQUE(student_id, class_id)
            )
        ''')
        
        # CBSE Syllabus Topics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cbse_topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grade INTEGER NOT NULL CHECK(grade >= 1 AND grade <= 12),
                chapter_number INTEGER,
                topic_name VARCHAR(200) NOT NULL,
                description TEXT,
                learning_objectives TEXT,
                prerequisites TEXT,
                difficulty_level VARCHAR(20) DEFAULT 'Medium',
                estimated_hours INTEGER DEFAULT 1,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Lessons
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER NOT NULL,
                title VARCHAR(200) NOT NULL,
                content_json TEXT NOT NULL,
                lesson_type VARCHAR(50) DEFAULT 'theory',
                duration_minutes INTEGER DEFAULT 45,
                is_published BOOLEAN DEFAULT 0,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES cbse_topics (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Activities
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER NOT NULL,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                activity_type VARCHAR(50) NOT NULL CHECK(activity_type IN ('MCQ', 'FillBlank', 'ShortAnswer', 'StepByStep', 'Simulation')),
                questions_json TEXT NOT NULL,
                max_score INTEGER DEFAULT 100,
                time_limit_minutes INTEGER,
                difficulty_level VARCHAR(20) DEFAULT 'Medium',
                is_published BOOLEAN DEFAULT 0,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES cbse_topics (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Student Activity Attempts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                answers_json TEXT NOT NULL,
                score INTEGER DEFAULT 0,
                max_score INTEGER NOT NULL,
                time_spent_minutes INTEGER DEFAULT 0,
                is_completed BOOLEAN DEFAULT 0,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (activity_id) REFERENCES activities (id),
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        ''')
        
        # Student Progress Tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                topic_id INTEGER NOT NULL,
                lessons_completed INTEGER DEFAULT 0,
                activities_completed INTEGER DEFAULT 0,
                total_score INTEGER DEFAULT 0,
                total_possible_score INTEGER DEFAULT 0,
                average_score REAL DEFAULT 0.0,
                time_spent_minutes INTEGER DEFAULT 0,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                mastery_level VARCHAR(20) DEFAULT 'Beginner',
                FOREIGN KEY (student_id) REFERENCES users (id),
                FOREIGN KEY (topic_id) REFERENCES cbse_topics (id),
                UNIQUE(student_id, topic_id)
            )
        ''')
        
        # Sessions for authentication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id VARCHAR(255) PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Settings/Configuration
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key VARCHAR(100) UNIQUE NOT NULL,
                setting_value TEXT,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_school ON users(school_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_classes_school_grade ON classes(school_id, grade)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_lessons_topic ON lessons(topic_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_activities_topic ON activities(topic_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attempts_student ON activity_attempts(student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_progress_student ON student_progress(student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id)')
        
        conn.commit()
        print("Database initialized successfully!")
    
    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Execute a SELECT query and return results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT query and return the last row id"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    
    def get_user_by_username(self, username: str) -> Optional[sqlite3.Row]:
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = ? AND is_active = 1"
        results = self.execute_query(query, (username,))
        return results[0] if results else None
    
    def get_user_by_id(self, user_id: int) -> Optional[sqlite3.Row]:
        """Get user by ID"""
        query = "SELECT * FROM users WHERE id = ? AND is_active = 1"
        results = self.execute_query(query, (user_id,))
        return results[0] if results else None
    
    def create_user(self, user_data: Dict[str, Any]) -> int:
        """Create a new user"""
        query = '''
            INSERT INTO users (username, email, password_hash, role, school_id, 
                             first_name, last_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            user_data['username'],
            user_data['email'],
            user_data['password_hash'],
            user_data['role'],
            user_data.get('school_id'),
            user_data.get('first_name'),
            user_data.get('last_name')
        )
        return self.execute_insert(query, params)
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> int:
        """Update user data"""
        set_clause = ", ".join([f"{key} = ?" for key in user_data.keys()])
        query = f"UPDATE users SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        params = tuple(user_data.values()) + (user_id,)
        return self.execute_update(query, params)
    
    def create_school(self, school_data: Dict[str, Any]) -> int:
        """Create a new school"""
        query = '''
            INSERT INTO schools (name, address, contact_email, contact_phone, admin_id)
            VALUES (?, ?, ?, ?, ?)
        '''
        params = (
            school_data['name'],
            school_data.get('address'),
            school_data.get('contact_email'),
            school_data.get('contact_phone'),
            school_data.get('admin_id')
        )
        return self.execute_insert(query, params)
    
    def get_schools(self) -> List[sqlite3.Row]:
        """Get all active schools"""
        query = "SELECT * FROM schools WHERE is_active = 1 ORDER BY name"
        return self.execute_query(query)
    
    def get_school_by_id(self, school_id: int) -> Optional[sqlite3.Row]:
        """Get school by ID"""
        query = "SELECT * FROM schools WHERE id = ? AND is_active = 1"
        results = self.execute_query(query, (school_id,))
        return results[0] if results else None