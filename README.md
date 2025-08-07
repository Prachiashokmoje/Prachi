# Mathematics Lab - Interactive Learning Platform

A comprehensive desktop application for mathematics education with role-based access control, CBSE syllabus integration, and interactive learning tools.

## Features

### User Roles
- **SuperAdmin**: Create schools, manage school admins
- **SchoolAdmin**: Create classes, teachers, students, map CBSE syllabus
- **Teacher**: Create/edit lessons and activities, view student progress
- **Student**: Access lessons, attempt activities, see feedback

### Core Functionality
- Secure authentication with hashed passwords
- Role-based access control and session management
- CBSE mathematics syllabus for grades 1-12
- Interactive simulations (geometry tools, number lines, graph plotting)
- Practice activities (MCQs, fill-in-the-blanks, short answers, step-by-step problems)
- Progress tracking and analytics
- Local-first data storage with export/import options

## Installation

1. Install Python 3.10+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python run.py
```

## Project Structure

```
mathematics_lab/
├── database/
│   ├── __init__.py
│   ├── models.py          # Database models and schema
│   ├── operations.py      # Database operations
│   └── init_db.py         # Database initialization
├── auth/
│   ├── __init__.py
│   ├── authentication.py  # Authentication logic
│   └── session.py         # Session management
├── content/
│   ├── __init__.py
│   ├── generator.py       # CBSE content generator
│   └── activities.py      # Activity management
├── ui/
│   ├── __init__.py
│   ├── templates/         # HTML templates
│   └── static/           # CSS, JS, assets
├── simulations/
│   ├── __init__.py
│   └── tools.py          # Interactive simulations
├── utils/
│   ├── __init__.py
│   └── helpers.py        # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_db.py
│   └── test_content.py
├── run.py                # Application entry point
└── requirements.txt
```

## Development Sprints

- **Sprint 1**: Database schema + authentication ✅
- **Sprint 2**: UI scaffolding
- **Sprint 3**: CBSE content generator
- **Sprint 4**: Activity player + analytics
- **Sprint 5**: Simulations and export/import features

## License

MIT License