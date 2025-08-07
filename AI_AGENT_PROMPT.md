# Mathematics Lab - AI Agent Development Prompt

## Project Overview
You are tasked with building a comprehensive Mathematics Lab application using Python, PyWebView, and SQLite. This application will serve as an interactive learning platform for CBSE mathematics curriculum (Grades 1-12) with role-based access control and extensive mathematical simulations.

## Technical Stack
- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript (with PyWebView)
- **Database**: SQLite
- **GUI Framework**: PyWebView
- **Mathematical Libraries**: NumPy, SciPy, SymPy, Matplotlib, Plotly
- **Authentication**: Flask-Login with bcrypt

## Core Requirements

### 1. Admin Panel (Super Admin)
**Functionality:**
- Create and manage multiple schools
- System-wide user management
- View analytics and reports
- Manage content and curriculum

**Key Features:**
- School registration and approval system
- User role assignment (admin, school_admin, teacher, student)
- System configuration and settings
- Backup and restore functionality

### 2. School Administration
**Functionality:**
- Manage teachers and students within their school
- Create and assign classes
- Monitor school-wide progress
- Content management for their school

**Key Features:**
- Teacher account creation and management
- Student enrollment and class assignment
- School-specific content customization
- Progress tracking and reporting

### 3. Class-wise Organization (CBSE Syllabus)
**Grade Structure:**
- **Primary (Grades 1-5)**: Numbers, Basic Operations, Shapes, Measurement, Money, Time
- **Middle (Grades 6-8)**: Number System, Algebra, Geometry, Mensuration, Data Handling
- **Secondary (Grades 9-10)**: Real Numbers, Polynomials, Linear Equations, Quadratic Equations, Trigonometry, Coordinate Geometry
- **Higher Secondary (Grades 11-12)**: Sets, Functions, Calculus, Statistics, Probability, Linear Programming

**Content Types:**
- Interactive Simulations
- Practice Exercises
- Assessment Quizzes
- Hands-on Activities
- Video Lessons
- Worksheets

### 4. Student Interface
**Core Features:**
- Personalized dashboard with progress tracking
- Interactive mathematical simulations
- Practice exercises with instant feedback
- Progress reports and analytics
- Achievement badges and gamification

**Simulation Types:**
- Number line operations
- Geometric shape manipulation
- Algebraic equation solving
- Statistical data visualization
- Fraction and decimal operations
- Coordinate geometry plotting

## Database Schema Implementation

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    school_id INTEGER,
    class_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    FOREIGN KEY (school_id) REFERENCES schools(id),
    FOREIGN KEY (class_id) REFERENCES classes(id)
);
```

### Schools Table
```sql
CREATE TABLE schools (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(120),
    website VARCHAR(200),
    admin_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id)
);
```

### Classes Table
```sql
CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    grade INTEGER NOT NULL,
    section VARCHAR(10),
    school_id INTEGER NOT NULL,
    teacher_id INTEGER,
    academic_year VARCHAR(20) NOT NULL DEFAULT '2024-25',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id),
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);
```

### Content Table
```sql
CREATE TABLE content (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    grade INTEGER NOT NULL,
    topic VARCHAR(100) NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    difficulty_level VARCHAR(20) DEFAULT 'beginner',
    file_path VARCHAR(500),
    html_content TEXT,
    js_code TEXT,
    css_styles TEXT,
    instructions TEXT,
    learning_objectives TEXT,
    prerequisites TEXT,
    estimated_duration INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### Progress Table
```sql
CREATE TABLE progress (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    content_id INTEGER NOT NULL,
    score FLOAT,
    max_score FLOAT DEFAULT 100.0,
    completed BOOLEAN DEFAULT FALSE,
    time_spent INTEGER,
    attempts INTEGER DEFAULT 1,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    feedback TEXT,
    notes TEXT,
    correct_answers INTEGER DEFAULT 0,
    total_questions INTEGER DEFAULT 0,
    accuracy FLOAT,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (content_id) REFERENCES content(id)
);
```

## Implementation Tasks

### Phase 1: Core Infrastructure
1. **Set up Flask application structure**
   - Create application factory
   - Configure database connections
   - Set up authentication system
   - Implement role-based access control

2. **Database Implementation**
   - Create all database models
   - Implement relationships and constraints
   - Add database migration scripts
   - Create seed data for testing

3. **Authentication System**
   - User registration and login
   - Password hashing and validation
   - Session management
   - Role-based route protection

### Phase 2: Admin and School Management
1. **Admin Panel**
   - School creation and management interface
   - User management dashboard
   - System configuration panel
   - Analytics and reporting

2. **School Administration**
   - Teacher and student account management
   - Class creation and assignment
   - School-specific settings
   - Progress monitoring tools

### Phase 3: Content Management
1. **Content Creation System**
   - Content upload and management interface
   - Grade and topic organization
   - Difficulty level assignment
   - Content preview and testing

2. **Mathematical Simulations**
   - Interactive number line
   - Geometric shape manipulator
   - Algebraic equation solver
   - Statistical data visualizer
   - Fraction and decimal calculator

### Phase 4: Student Interface
1. **Student Dashboard**
   - Personalized content recommendations
   - Progress tracking and visualization
   - Achievement system
   - Learning path guidance

2. **Interactive Learning**
   - Simulation interfaces
   - Practice exercise system
   - Instant feedback mechanism
   - Progress saving and retrieval

### Phase 5: Teacher Interface
1. **Teacher Dashboard**
   - Class management
   - Student progress monitoring
   - Content assignment tools
   - Assessment creation

2. **Reporting and Analytics**
   - Student performance reports
   - Class progress analytics
   - Content effectiveness metrics
   - Learning outcome tracking

## Mathematical Content Requirements

### Grade 1-2 (Primary)
- **Numbers**: Counting, Number recognition, Number line
- **Addition/Subtraction**: Basic operations, Word problems
- **Shapes**: Basic geometric shapes, Pattern recognition
- **Measurement**: Length, Weight, Capacity
- **Money**: Indian currency, Simple calculations

### Grade 3-5 (Upper Primary)
- **Numbers**: Place value, Rounding, Estimation
- **Operations**: Multiplication, Division, Fractions
- **Geometry**: Angles, Perimeter, Area
- **Data Handling**: Pictographs, Bar graphs
- **Decimals**: Decimal operations, Money calculations

### Grade 6-8 (Middle School)
- **Number System**: Integers, Rational numbers
- **Algebra**: Variables, Simple equations
- **Geometry**: Triangles, Circles, Mensuration
- **Statistics**: Mean, Median, Mode
- **Practical Geometry**: Constructions

### Grade 9-10 (Secondary)
- **Real Numbers**: Irrational numbers, Number line
- **Polynomials**: Factorization, Algebraic identities
- **Linear Equations**: Pair of linear equations
- **Quadratic Equations**: Factorization, Formula
- **Trigonometry**: Trigonometric ratios, Heights and distances
- **Coordinate Geometry**: Distance formula, Section formula
- **Geometry**: Similar triangles, Circles, Constructions

### Grade 11-12 (Higher Secondary)
- **Sets and Functions**: Set operations, Function types
- **Algebra**: Complex numbers, Linear inequalities
- **Calculus**: Limits, Derivatives, Applications
- **Statistics**: Probability, Random variables
- **Linear Programming**: Optimization problems

## Interactive Simulation Examples

### 1. Number Line Simulation
- Drag and drop numbers on number line
- Visual addition and subtraction
- Fraction and decimal placement
- Interactive number comparisons

### 2. Geometric Shape Manipulator
- Drag vertices to change shapes
- Real-time area and perimeter calculation
- Angle measurement tools
- Shape transformation animations

### 3. Algebraic Equation Solver
- Balance scale visualization
- Step-by-step solution display
- Variable manipulation
- Graph plotting for equations

### 4. Statistical Data Visualizer
- Interactive bar charts and histograms
- Mean, median, mode calculation
- Data point manipulation
- Probability simulations

### 5. Fraction Calculator
- Visual fraction representation
- Addition, subtraction, multiplication
- Equivalent fraction finder
- Mixed number operations

## UI/UX Requirements

### Design Principles
- **Responsive Design**: Works on different screen sizes
- **Accessibility**: WCAG 2.1 compliance
- **Intuitive Navigation**: Clear menu structure
- **Visual Feedback**: Immediate response to user actions
- **Progress Indication**: Clear learning progress visualization

### Color Scheme
- **Primary**: Blue (#007bff) - Trust and education
- **Secondary**: Green (#28a745) - Success and growth
- **Warning**: Orange (#ffc107) - Attention and caution
- **Danger**: Red (#dc3545) - Errors and important alerts
- **Info**: Cyan (#17a2b8) - Information and guidance

### Typography
- **Headings**: Clear hierarchy with sans-serif fonts
- **Body Text**: Readable font size (16px minimum)
- **Mathematical Notation**: LaTeX rendering support
- **Icons**: Consistent icon set for navigation

## Testing Requirements

### Unit Testing
- Database model testing
- Authentication system testing
- Mathematical utility function testing
- API endpoint testing

### Integration Testing
- User workflow testing
- Role-based access testing
- Content creation and assignment testing
- Progress tracking testing

### User Acceptance Testing
- Student learning experience testing
- Teacher content management testing
- Admin system management testing
- Cross-browser compatibility testing

## Deployment Considerations

### Development Environment
- Python virtual environment
- SQLite database for development
- Hot reload for development
- Debug mode enabled

### Production Environment
- Secure database configuration
- Environment variable management
- Logging and monitoring
- Backup and recovery procedures

## Security Requirements

### Authentication Security
- Password hashing with bcrypt
- Session management
- CSRF protection
- Rate limiting for login attempts

### Data Security
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- Secure file upload handling

### Access Control
- Role-based permissions
- Resource-level access control
- Audit logging
- Secure API endpoints

## Performance Requirements

### Response Time
- Page load time < 3 seconds
- API response time < 1 second
- Database query optimization
- Caching for frequently accessed data

### Scalability
- Support for multiple schools
- Concurrent user handling
- Database connection pooling
- Resource optimization

## Documentation Requirements

### Technical Documentation
- API documentation
- Database schema documentation
- Deployment guide
- Troubleshooting guide

### User Documentation
- Student user guide
- Teacher user guide
- Admin user guide
- Content creation guide

## Success Metrics

### Learning Outcomes
- Student engagement metrics
- Progress completion rates
- Assessment performance improvement
- Time spent on learning activities

### System Performance
- User adoption rates
- System uptime and reliability
- Response time metrics
- Error rate monitoring

## Development Timeline

### Week 1-2: Foundation
- Project setup and configuration
- Database schema implementation
- Basic authentication system
- Core application structure

### Week 3-4: Admin System
- Admin panel development
- School management interface
- User management system
- Basic reporting

### Week 5-6: Content Management
- Content creation interface
- Mathematical simulation framework
- Grade-wise content organization
- Content assignment system

### Week 7-8: Student Interface
- Student dashboard development
- Interactive simulation implementation
- Progress tracking system
- Assessment and feedback system

### Week 9-10: Teacher Interface
- Teacher dashboard development
- Class management tools
- Student progress monitoring
- Content assignment interface

### Week 11-12: Testing and Polish
- Comprehensive testing
- Bug fixes and optimization
- Documentation completion
- Deployment preparation

## Additional Considerations

### Accessibility
- Screen reader compatibility
- Keyboard navigation support
- High contrast mode
- Font size adjustment options

### Internationalization
- Multi-language support preparation
- Currency and number format localization
- Date and time format handling
- Cultural adaptation considerations

### Mobile Responsiveness
- Touch-friendly interface
- Mobile-optimized simulations
- Responsive design implementation
- Offline capability considerations

This comprehensive prompt provides the AI agent with all necessary information to build a complete Mathematics Lab application. The agent should follow this structure systematically, ensuring each component is properly implemented and integrated with the overall system.