# Mathematics Lab Application

A comprehensive mathematics learning platform built with Python 3.10+, pywebview, and SQLite. This desktop application supports multiple user roles and provides an interactive learning environment for CBSE mathematics curriculum.

## Features

### User Roles
- **SuperAdmin**: Create and manage schools, manage school administrators
- **SchoolAdmin**: Create classes, manage teachers and students, map CBSE syllabus
- **Teacher**: Create/edit lessons and activities, view student progress
- **Student**: Access lessons, attempt activities, receive feedback

### Core Functionality
- **Secure Authentication**: Password hashing with bcrypt, role-based access control
- **Session Management**: Secure session handling with automatic cleanup
- **School Management**: Multi-school support with hierarchical permissions
- **CBSE Curriculum Mapping**: Complete syllabus mapping for grades 1-12
- **Interactive Learning**: Lessons with theory, examples, and practice activities
- **Progress Tracking**: Comprehensive analytics and progress monitoring
- **Local-First Data**: All data stored locally in SQLite database

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python run.py
```

## Development Status

This project is developed in sprints:

### ✅ Sprint 1 - Database Schema + Authentication (COMPLETED)
- SQLite database with complete schema
- User authentication with bcrypt password hashing
- Role-based access control (SuperAdmin, SchoolAdmin, Teacher, Student)
- Session management with automatic cleanup
- Comprehensive unit tests for database and authentication

### 🚧 Sprint 2 - UI Scaffolding (IN PROGRESS)
- PyWebview-based desktop application
- HTML/CSS/JavaScript frontend
- Role-based navigation and dashboards
- Responsive design with accessibility features

### 📋 Sprint 3 - CBSE Content Generator (PLANNED)
- JSON-based lesson content structure
- Activity generator for different question types
- CBSE syllabus mapping for all grades
- Sample content for grades 1, 6, 9, and 12

### 📋 Sprint 4 - Activity Player + Analytics (PLANNED)
- Interactive activity player
- MCQ, Fill-in-blanks, Short answers, Step-by-step problems
- Immediate feedback and scoring
- Progress tracking and analytics

### 📋 Sprint 5 - Simulations + Export/Import (PLANNED)
- Interactive simulations (geometry tools, number lines, graph plotting)
- Data export/import functionality
- Advanced accessibility features
- Performance optimizations

## Project Structure

```
mathematics-lab/
├── src/
│   ├── database/
│   │   ├── __init__.py
│   │   └── db_manager.py          # Database operations and schema
│   ├── auth/
│   │   ├── __init__.py
│   │   └── auth_manager.py        # Authentication and session management
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── app_controller.py      # PyWebview controller and API
│   │   └── templates/
│   │       └── index.html         # Main HTML interface
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py              # Authentication tests
│   └── test_database.py         # Database tests
├── data/
│   └── mathlab.db               # SQLite database (created on first run)
├── requirements.txt             # Python dependencies
├── run.py                      # Main application entry point
└── README.md                   # This file
```

## Database Schema

The application uses SQLite with the following main tables:

- **users**: User accounts with roles and authentication data
- **schools**: School information and admin assignments
- **classes**: Class/grade information linked to schools
- **cbse_topics**: CBSE syllabus topics for each grade
- **lessons**: Lesson content in JSON format
- **activities**: Practice activities and assessments
- **activity_attempts**: Student attempt records
- **student_progress**: Progress tracking per student/topic
- **user_sessions**: Session management for authentication

## Default Login

On first run, a default SuperAdmin account is created:
- **Username**: admin
- **Password**: admin123

⚠️ **Important**: Change the default password immediately after first login.

## Testing

Run the unit tests to verify functionality:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_auth.py
python -m pytest tests/test_database.py

# Run with coverage
python -m pytest --cov=src tests/
```

## Development Guidelines

### Adding New Features
1. Create feature branch from main
2. Write unit tests first (TDD approach)
3. Implement feature following existing patterns
4. Update documentation
5. Submit pull request

### Database Changes
- Always create migration scripts for schema changes
- Update test database setup accordingly
- Ensure backward compatibility when possible

### Authentication & Security
- All passwords must be hashed with bcrypt
- Session validation required for protected endpoints
- Role-based access control enforced at multiple levels

## Configuration

The application uses minimal configuration. Database path and session duration can be modified in the respective manager classes:

- Database path: `DatabaseManager.__init__()`
- Session duration: `AuthManager.session_duration_hours`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Implement the feature
5. Run all tests to ensure nothing breaks
6. Submit a pull request

## License

This project is developed for educational purposes. Please ensure compliance with your organization's policies before deployment.

## Support

For issues or questions:
1. Check existing test cases for usage examples
2. Review the database schema in `db_manager.py`
3. Check authentication flows in `auth_manager.py`
4. Create an issue with detailed description and steps to reproduce

## Roadmap

### Phase 1 (Current)
- ✅ Core authentication and database foundation
- 🚧 Basic UI and navigation

### Phase 2 (Next)
- CBSE content management system
- Lesson creation and editing tools
- Basic activity types (MCQ, Fill-in-blanks)

### Phase 3 (Future)
- Advanced interactive simulations
- Comprehensive analytics dashboard
- Mobile-responsive improvements
- Offline synchronization capabilities

---

**Mathematics Lab** - Making mathematics learning interactive and engaging for students while providing powerful tools for educators and administrators.