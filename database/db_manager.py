"""
Database Manager for Mathematics Lab Application
Handles all database operations using SQLite
"""

import sqlite3
import json
import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

class DatabaseManager:
    """Manages all database operations for the Mathematics Lab application"""
    
    def __init__(self, db_path: str = "mathematics_lab.db"):
        """Initialize database manager"""
        self.db_path = db_path
        self.connection = None
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        self.db_path = str(data_dir / "mathematics_lab.db")
    
    def get_connection(self):
        """Get database connection"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def create_tables(self):
        """Create all database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                role VARCHAR(20) NOT NULL CHECK (role IN ('super_admin', 'school_admin', 'teacher', 'student')),
                school_id INTEGER,
                class_id INTEGER,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                FOREIGN KEY (school_id) REFERENCES schools(id),
                FOREIGN KEY (class_id) REFERENCES classes(id)
            )
        """)
        
        # Schools table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                address TEXT NOT NULL,
                city VARCHAR(100) NOT NULL,
                state VARCHAR(100) NOT NULL,
                pincode VARCHAR(10) NOT NULL,
                phone VARCHAR(20),
                email VARCHAR(100),
                website VARCHAR(200),
                admin_id INTEGER,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (admin_id) REFERENCES users(id)
            )
        """)
        
        # Classes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                grade INTEGER NOT NULL CHECK (grade >= 1 AND grade <= 12),
                section VARCHAR(10),
                school_id INTEGER NOT NULL,
                teacher_id INTEGER,
                academic_year VARCHAR(20) DEFAULT '2024-25',
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_id) REFERENCES schools(id),
                FOREIGN KEY (teacher_id) REFERENCES users(id)
            )
        """)
        
        # Topics table (CBSE syllabus)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                grade INTEGER NOT NULL CHECK (grade >= 1 AND grade <= 12),
                description TEXT,
                order_index INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Lessons table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                topic_id INTEGER NOT NULL,
                content JSON NOT NULL,
                objectives TEXT,
                prerequisites TEXT,
                estimated_duration INTEGER, -- in minutes
                created_by INTEGER NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)
        
        # Activities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                lesson_id INTEGER NOT NULL,
                activity_type VARCHAR(50) NOT NULL CHECK (activity_type IN ('mcq', 'fill_blank', 'short_answer', 'step_by_step', 'simulation')),
                content JSON NOT NULL,
                max_score INTEGER DEFAULT 100,
                time_limit INTEGER, -- in minutes
                created_by INTEGER NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lesson_id) REFERENCES lessons(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)
        
        # Student attempts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                activity_id INTEGER NOT NULL,
                score INTEGER,
                max_score INTEGER DEFAULT 100,
                time_spent INTEGER, -- in seconds
                answers JSON,
                feedback TEXT,
                completed BOOLEAN DEFAULT 0,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(id),
                FOREIGN KEY (activity_id) REFERENCES activities(id)
            )
        """)
        
        # Student progress table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                topic_id INTEGER NOT NULL,
                lessons_completed INTEGER DEFAULT 0,
                total_lessons INTEGER DEFAULT 0,
                activities_completed INTEGER DEFAULT 0,
                total_activities INTEGER DEFAULT 0,
                average_score FLOAT DEFAULT 0,
                total_time_spent INTEGER DEFAULT 0, -- in minutes
                last_activity_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(id),
                FOREIGN KEY (topic_id) REFERENCES topics(id),
                UNIQUE(student_id, topic_id)
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_school ON users(school_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_classes_school ON classes(school_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_lessons_topic ON lessons(topic_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_activities_lesson ON activities(lesson_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_attempts_student ON student_attempts(student_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_progress_student ON student_progress(student_id)")
        
        conn.commit()
        print("✅ Database tables created successfully")
    
    def create_sample_data(self):
        """Create sample data for testing"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create sample school
        cursor.execute("""
            INSERT OR IGNORE INTO schools (name, address, city, state, pincode, phone, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("Delhi Public School", "123 Education Street", "New Delhi", "Delhi", "110001", "011-12345678", "info@dps.edu.in"))
        
        school_id = cursor.lastrowid or 1
        
        # Create super admin
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, email, password_hash, first_name, last_name, role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("admin", "admin@mathlab.com", password_hash, "Super", "Admin", "super_admin"))
        
        # Create school admin
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, email, password_hash, first_name, last_name, role, school_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("schooladmin", "admin@dps.edu.in", password_hash, "School", "Administrator", "school_admin", school_id))
        
        # Create sample teacher
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, email, password_hash, first_name, last_name, role, school_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("teacher1", "teacher@dps.edu.in", password_hash, "Mathematics", "Teacher", "teacher", school_id))
        
        # Create sample class
        cursor.execute("""
            INSERT OR IGNORE INTO classes (name, grade, section, school_id, teacher_id)
            VALUES (?, ?, ?, ?, ?)
        """, ("Class 10A", 10, "A", school_id, 3))  # teacher_id = 3
        
        # Create sample student
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, email, password_hash, first_name, last_name, role, school_id, class_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("student1", "student@dps.edu.in", password_hash, "John", "Doe", "student", school_id, 1))
        
        # Create CBSE topics for sample grades
        topics_data = [
            # Grade 1
            ("Numbers 1-100", 1, "Counting and number recognition", 1),
            ("Addition", 1, "Basic addition operations", 2),
            ("Subtraction", 1, "Basic subtraction operations", 3),
            ("Shapes", 1, "Basic geometric shapes", 4),
            
            # Grade 6
            ("Number System", 6, "Integers and rational numbers", 1),
            ("Algebra", 6, "Variables and simple equations", 2),
            ("Geometry", 6, "Basic geometric concepts", 3),
            ("Mensuration", 6, "Perimeter and area", 4),
            
            # Grade 9
            ("Real Numbers", 9, "Irrational numbers and number line", 1),
            ("Polynomials", 9, "Polynomial operations and factorization", 2),
            ("Linear Equations", 9, "Pair of linear equations", 3),
            ("Coordinate Geometry", 9, "Distance formula and section formula", 4),
            
            # Grade 12
            ("Relations and Functions", 12, "Set operations and function types", 1),
            ("Calculus", 12, "Limits, derivatives, and applications", 2),
            ("Statistics", 12, "Probability and random variables", 3),
            ("Linear Programming", 12, "Optimization problems", 4),
        ]
        
        for topic_name, grade, description, order_idx in topics_data:
            cursor.execute("""
                INSERT OR IGNORE INTO topics (name, grade, description, order_index)
                VALUES (?, ?, ?, ?)
            """, (topic_name, grade, description, order_idx))
        
        conn.commit()
        print("✅ Sample data created successfully")
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND is_active = 1", (username,))
        user = cursor.fetchone()
        return dict(user) if user else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ? AND is_active = 1", (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None
    
    def create_user(self, user_data: Dict) -> int:
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, first_name, last_name, role, school_id, class_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_data['username'],
            user_data['email'],
            user_data['password_hash'],
            user_data['first_name'],
            user_data['last_name'],
            user_data['role'],
            user_data.get('school_id'),
            user_data.get('class_id')
        ))
        
        conn.commit()
        return cursor.lastrowid
    
    def update_user_last_login(self, user_id: int):
        """Update user's last login time"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (user_id,))
        conn.commit()
    
    def get_schools(self) -> List[Dict]:
        """Get all schools"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM schools WHERE is_active = 1 ORDER BY name")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_classes_by_school(self, school_id: int) -> List[Dict]:
        """Get classes for a school"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, u.first_name, u.last_name as teacher_name 
            FROM classes c 
            LEFT JOIN users u ON c.teacher_id = u.id 
            WHERE c.school_id = ? AND c.is_active = 1 
            ORDER BY c.grade, c.section
        """, (school_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_topics_by_grade(self, grade: int) -> List[Dict]:
        """Get topics for a specific grade"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM topics 
            WHERE grade = ? AND is_active = 1 
            ORDER BY order_index
        """, (grade,))
        return [dict(row) for row in cursor.fetchall()]
    
    def __del__(self):
        """Cleanup on deletion"""
        self.close_connection()