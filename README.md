# Mathematics Lab - Interactive Learning Platform

A comprehensive Mathematics Lab application built with Python, PyWebView, and SQLite for CBSE curriculum (Grades 1-12).

## Features

### 1. Admin Panel
- Create and manage schools
- User authentication system
- Role-based access control

### 2. School Administration
- Create teacher and student accounts
- Manage class assignments
- Monitor student progress

### 3. Class-wise Organization
- CBSE syllabus alignment (Grades 1-12)
- Structured content by class and topic
- Progressive difficulty levels

### 4. Student Interface
- Interactive mathematical simulations
- Practice exercises and activities
- Progress tracking and analytics

## Project Structure

```
mathematics_lab/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── school.py
│   │   ├── class.py
│   │   ├── content.py
│   │   └── progress.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── school.py
│   │   ├── student.py
│   │   └── teacher.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   │   ├── admin/
│   │   ├── auth/
│   │   ├── school/
│   │   ├── student/
│   │   └── teacher/
│   └── utils/
│       ├── __init__.py
│       ├── database.py
│       ├── auth_utils.py
│       └── math_utils.py
├── simulations/
│   ├── grade1/
│   ├── grade2/
│   └── ...
├── content/
│   ├── grade1/
│   ├── grade2/
│   └── ...
├── database/
│   └── mathlab.db
├── main.py
├── requirements.txt
└── README.md
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Database Schema

### Users Table
- id, username, email, password_hash, role, school_id, created_at

### Schools Table
- id, name, address, admin_id, created_at

### Classes Table
- id, name, grade, school_id, teacher_id

### Content Table
- id, title, description, grade, topic, content_type, file_path

### Progress Table
- id, student_id, content_id, score, completed_at

## CBSE Syllabus Coverage

### Grade 1-5 (Primary)
- Numbers and Operations
- Geometry
- Measurement
- Data Handling

### Grade 6-8 (Middle)
- Algebra
- Geometry
- Mensuration
- Statistics

### Grade 9-10 (Secondary)
- Real Numbers
- Polynomials
- Linear Equations
- Quadratic Equations
- Trigonometry

### Grade 11-12 (Higher Secondary)
- Sets and Functions
- Algebra
- Calculus
- Statistics and Probability