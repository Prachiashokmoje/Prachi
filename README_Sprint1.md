# Mathematics Lab - Sprint 1: Database Schema & Authentication

## 🎯 Sprint Overview

**Sprint 1** focuses on establishing the core foundation of the Mathematics Lab application with:
- Complete SQLite database schema
- Secure authentication system
- Role-based access control
- Basic UI scaffolding with pywebview

## 📁 Project Structure

```
mathematics_lab/
├── run.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── database/
│   ├── __init__.py
│   └── db_manager.py      # Database operations and schema
├── auth/
│   ├── __init__.py
│   └── auth_manager.py    # Authentication and authorization
├── ui/
│   ├── __init__.py
│   └── app_ui.py         # UI generation and JavaScript API
├── tests/
│   ├── __init__.py
│   └── test_sprint1.py   # Unit tests for Sprint 1
├── data/                 # SQLite database storage
└── README_Sprint1.md     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python run.py
   ```

4. **Login with sample credentials:**
   - **Super Admin**: `admin` / `admin123`
   - **School Admin**: `schooladmin` / `school123`
   - **Teacher**: `teacher1` / `teacher123`
   - **Student**: `student1` / `student123`

## 🗄️ Database Schema

### Core Tables

#### 1. Users Table
```sql
CREATE TABLE users (
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
);
```

#### 2. Schools Table
```sql
CREATE TABLE schools (
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
);
```

#### 3. Classes Table
```sql
CREATE TABLE classes (
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
);
```

#### 4. Topics Table (CBSE Syllabus)
```sql
CREATE TABLE topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    grade INTEGER NOT NULL CHECK (grade >= 1 AND grade <= 12),
    description TEXT,
    order_index INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5. Lessons Table
```sql
CREATE TABLE lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    topic_id INTEGER NOT NULL,
    content JSON NOT NULL,
    objectives TEXT,
    prerequisites TEXT,
    estimated_duration INTEGER,
    created_by INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES topics(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

#### 6. Activities Table
```sql
CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    lesson_id INTEGER NOT NULL,
    activity_type VARCHAR(50) NOT NULL CHECK (activity_type IN ('mcq', 'fill_blank', 'short_answer', 'step_by_step', 'simulation')),
    content JSON NOT NULL,
    max_score INTEGER DEFAULT 100,
    time_limit INTEGER,
    created_by INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

#### 7. Student Attempts Table
```sql
CREATE TABLE student_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    activity_id INTEGER NOT NULL,
    score INTEGER,
    max_score INTEGER DEFAULT 100,
    time_spent INTEGER,
    answers JSON,
    feedback TEXT,
    completed BOOLEAN DEFAULT 0,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (activity_id) REFERENCES activities(id)
);
```

#### 8. Student Progress Table
```sql
CREATE TABLE student_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    lessons_completed INTEGER DEFAULT 0,
    total_lessons INTEGER DEFAULT 0,
    activities_completed INTEGER DEFAULT 0,
    total_activities INTEGER DEFAULT 0,
    average_score FLOAT DEFAULT 0,
    total_time_spent INTEGER DEFAULT 0,
    last_activity_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (topic_id) REFERENCES topics(id),
    UNIQUE(student_id, topic_id)
);
```

## 🔐 Authentication System

### Features
- **Secure Password Hashing**: SHA-256 with salt
- **Session Management**: 8-hour session tokens
- **Role-Based Access Control**: 4 distinct user roles
- **Input Validation**: Comprehensive validation for all inputs

### User Roles

#### 1. Super Admin
- **Permissions**: Full system access
- **Capabilities**:
  - Create and manage schools
  - Manage all users across schools
  - System-wide analytics and reports
  - Database administration

#### 2. School Admin
- **Permissions**: School-specific access
- **Capabilities**:
  - Manage teachers and students in their school
  - Create and assign classes
  - School-specific content management
  - School analytics and reports

#### 3. Teacher
- **Permissions**: Class and content management
- **Capabilities**:
  - Manage assigned classes
  - Create and edit lessons and activities
  - View student progress and analytics
  - Content assignment and assessment

#### 4. Student
- **Permissions**: Learning interface access
- **Capabilities**:
  - Access assigned lessons and activities
  - Complete interactive exercises
  - View personal progress and analytics
  - Submit assignments and assessments

## 🎨 User Interface

### Features
- **Responsive Design**: Works on different screen sizes
- **High Contrast Mode**: Accessibility feature
- **Keyboard Navigation**: Full keyboard support
- **Modern UI**: Bootstrap 5 with custom styling
- **Role-Based Navigation**: Dynamic sidebar based on user role

### UI Components
- **Login Screen**: Secure authentication interface
- **Dashboard**: Role-specific overview and statistics
- **Sidebar Navigation**: Context-aware menu system
- **Data Tables**: Sortable and searchable data display
- **Alert System**: User feedback and notifications

## 🧪 Testing

### Running Tests
```bash
python tests/test_sprint1.py
```

### Test Coverage
- **Database Operations**: Table creation, CRUD operations, relationships
- **Authentication**: Login/logout, password hashing, role checking
- **User Management**: User creation, validation, permissions
- **Data Integrity**: Foreign key constraints, data validation

### Test Results
All tests should pass with the following output:
```
🧪 Running Sprint 1 Tests...
==================================================
✅ Database table creation test passed
✅ Sample data creation test passed
✅ User operations test passed
✅ School operations test passed
✅ Topic operations test passed
✅ Password hashing test passed
✅ Login/logout test passed
✅ Failed login test passed
✅ Role checking test passed
✅ User creation test passed
✅ Permissions test passed
==================================================
🎉 All Sprint 1 tests passed!
```

## 📊 Sample Data

### Pre-loaded Content
- **1 Sample School**: Delhi Public School
- **4 User Accounts**: One for each role
- **1 Sample Class**: Class 10A
- **16 CBSE Topics**: 4 topics each for grades 1, 6, 9, and 12

### CBSE Topics by Grade

#### Grade 1
1. Numbers 1-100
2. Addition
3. Subtraction
4. Shapes

#### Grade 6
1. Number System
2. Algebra
3. Geometry
4. Mensuration

#### Grade 9
1. Real Numbers
2. Polynomials
3. Linear Equations
4. Coordinate Geometry

#### Grade 12
1. Relations and Functions
2. Calculus
3. Statistics
4. Linear Programming

## 🔧 Configuration

### Database Configuration
- **Database Type**: SQLite
- **Location**: `data/mathematics_lab.db`
- **Auto-creation**: Database and tables created automatically
- **Sample Data**: Pre-loaded for testing

### Security Configuration
- **Password Hashing**: SHA-256
- **Session Duration**: 8 hours
- **Input Validation**: Comprehensive validation
- **SQL Injection Protection**: Parameterized queries

## 🚀 Next Steps (Sprint 2)

### Planned Features
1. **Enhanced UI Components**: Forms, modals, and interactive elements
2. **Data Management**: CRUD operations for all entities
3. **Search and Filter**: Advanced data querying
4. **Export/Import**: Data backup and restore functionality
5. **User Management**: Complete user administration interface

### Technical Improvements
1. **Error Handling**: Comprehensive error management
2. **Logging**: Application logging and debugging
3. **Performance**: Query optimization and caching
4. **Security**: Additional security measures
5. **Documentation**: API documentation and user guides

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: Module not found errors
**Solution**: Ensure you're running from the project root directory

#### 2. Database Errors
**Problem**: Database connection issues
**Solution**: Check file permissions for the `data/` directory

#### 3. PyWebView Issues
**Problem**: Application won't start
**Solution**: Ensure pywebview is properly installed and system dependencies are met

#### 4. Login Issues
**Problem**: Can't login with sample credentials
**Solution**: Run the application fresh to ensure sample data is created

### Getting Help
- Check the console output for error messages
- Verify all dependencies are installed
- Ensure you're using Python 3.10+
- Test with the provided unit tests

## 📝 License

This project is developed for educational purposes as part of the Mathematics Lab application.

---

**Sprint 1 Status**: ✅ **COMPLETED**
**Next Sprint**: Sprint 2 - Enhanced UI and Data Management