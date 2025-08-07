"""
Application UI Manager for Mathematics Lab
Handles HTML generation and JavaScript API for pywebview
"""

import json
from typing import Dict, Any, Optional
from auth.auth_manager import AuthManager
from database.db_manager import DatabaseManager

class MathematicsLabUI:
    """Manages the user interface for the Mathematics Lab application"""
    
    def __init__(self, auth_manager: AuthManager, db_manager: DatabaseManager):
        """Initialize UI manager"""
        self.auth_manager = auth_manager
        self.db_manager = db_manager
    
    def get_main_html(self) -> str:
        """Get the main HTML content for the application"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mathematics Lab - Interactive Learning Platform</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #007bff;
            --secondary-color: #6c757d;
            --success-color: #28a745;
            --danger-color: #dc3545;
            --warning-color: #ffc107;
            --info-color: #17a2b8;
            --light-color: #f8f9fa;
            --dark-color: #343a40;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 0;
        }}
        
        .app-container {{
            display: flex;
            min-height: 100vh;
        }}
        
        .sidebar {{
            width: 280px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }}
        
        .main-content {{
            flex: 1;
            display: flex;
            flex-direction: column;
        }}
        
        .top-navbar {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .content-area {{
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
        }}
        
        .login-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 2rem;
        }}
        
        .login-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            max-width: 400px;
            width: 100%;
        }}
        
        .login-header {{
            background: linear-gradient(135deg, var(--primary-color) 0%, #0056b3 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }}
        
        .login-body {{
            padding: 2rem;
        }}
        
        .form-control {{
            border-radius: 10px;
            border: 2px solid #e9ecef;
            padding: 12px 15px;
            transition: all 0.3s ease;
        }}
        
        .form-control:focus {{
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, var(--primary-color) 0%, #0056b3 100%);
            border: none;
            border-radius: 10px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 123, 255, 0.4);
        }}
        
        .sidebar-header {{
            padding: 1.5rem;
            border-bottom: 1px solid #e9ecef;
            text-align: center;
        }}
        
        .sidebar-nav {{
            padding: 1rem 0;
        }}
        
        .nav-item {{
            margin: 0.25rem 1rem;
        }}
        
        .nav-link {{
            display: flex;
            align-items: center;
            padding: 0.75rem 1rem;
            color: var(--dark-color);
            text-decoration: none;
            border-radius: 10px;
            transition: all 0.3s ease;
        }}
        
        .nav-link:hover {{
            background: rgba(0, 123, 255, 0.1);
            color: var(--primary-color);
        }}
        
        .nav-link.active {{
            background: var(--primary-color);
            color: white;
        }}
        
        .nav-link i {{
            margin-right: 0.75rem;
            width: 20px;
        }}
        
        .dashboard-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, var(--primary-color) 0%, #0056b3 100%);
            color: white;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            opacity: 0.9;
        }}
        
        .alert {{
            border-radius: 10px;
            border: none;
            padding: 1rem 1.5rem;
        }}
        
        .table {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            overflow: hidden;
        }}
        
        .table th {{
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 1rem;
        }}
        
        .table td {{
            padding: 1rem;
            border-color: rgba(0, 0, 0, 0.1);
        }}
        
        .hidden {{
            display: none !important;
        }}
        
        /* High contrast mode */
        .high-contrast {{
            background: #000 !important;
            color: #fff !important;
        }}
        
        .high-contrast .sidebar,
        .high-contrast .top-navbar,
        .high-contrast .dashboard-card,
        .high-contrast .login-card {{
            background: #000 !important;
            color: #fff !important;
            border: 2px solid #fff !important;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .sidebar {{
                width: 100%;
                position: fixed;
                top: 0;
                left: -100%;
                transition: left 0.3s ease;
                z-index: 1001;
            }}
            
            .sidebar.show {{
                left: 0;
            }}
            
            .main-content {{
                margin-left: 0;
            }}
        }}
    </style>
</head>
<body>
    <div id="app">
        <!-- Login Screen -->
        <div id="loginScreen" class="login-container">
            <div class="login-card">
                <div class="login-header">
                    <i class="fas fa-calculator fa-3x mb-3"></i>
                    <h2>Mathematics Lab</h2>
                    <p class="mb-0">Interactive Learning Platform</p>
                </div>
                <div class="login-body">
                    <div id="loginAlert" class="alert alert-danger hidden" role="alert"></div>
                    <form id="loginForm">
                        <div class="mb-3">
                            <label for="username" class="form-label">Username</label>
                            <div class="input-group">
                                <span class="input-group-text">
                                    <i class="fas fa-user"></i>
                                </span>
                                <input type="text" class="form-control" id="username" name="username" required>
                            </div>
                        </div>
                        <div class="mb-4">
                            <label for="password" class="form-label">Password</label>
                            <div class="input-group">
                                <span class="input-group-text">
                                    <i class="fas fa-lock"></i>
                                </span>
                                <input type="password" class="form-control" id="password" name="password" required>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">
                            <i class="fas fa-sign-in-alt me-2"></i>Login
                        </button>
                    </form>
                    <div class="text-center mt-4">
                        <p class="text-muted">
                            <i class="fas fa-info-circle me-1"></i>
                            Contact your administrator for login credentials
                        </p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Main Application -->
        <div id="mainApp" class="app-container hidden">
            <!-- Sidebar -->
            <div class="sidebar">
                <div class="sidebar-header">
                    <i class="fas fa-calculator fa-2x text-primary mb-2"></i>
                    <h5 class="mb-0">Mathematics Lab</h5>
                    <small class="text-muted" id="userInfo">Welcome!</small>
                </div>
                <nav class="sidebar-nav" id="sidebarNav">
                    <!-- Navigation items will be populated by JavaScript -->
                </nav>
            </div>
            
            <!-- Main Content -->
            <div class="main-content">
                <!-- Top Navigation -->
                <div class="top-navbar">
                    <div class="d-flex align-items-center">
                        <button class="btn btn-outline-primary me-3 d-md-none" id="sidebarToggle">
                            <i class="fas fa-bars"></i>
                        </button>
                        <h4 class="mb-0" id="pageTitle">Dashboard</h4>
                    </div>
                    <div class="d-flex align-items-center">
                        <button class="btn btn-outline-secondary me-2" id="highContrastToggle">
                            <i class="fas fa-adjust"></i>
                        </button>
                        <button class="btn btn-outline-danger" id="logoutBtn">
                            <i class="fas fa-sign-out-alt me-1"></i>Logout
                        </button>
                    </div>
                </div>
                
                <!-- Content Area -->
                <div class="content-area" id="contentArea">
                    <!-- Content will be loaded here -->
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Global variables
        let currentUser = null;
        let currentView = 'dashboard';
        
        // Initialize application
        document.addEventListener('DOMContentLoaded', function() {{
            initializeApp();
        }});
        
        function initializeApp() {{
            // Check if user is already logged in
            pywebview.api.checkAuth().then(function(response) {{
                if (response.authenticated) {{
                    currentUser = response.user;
                    showMainApp();
                    loadDashboard();
                }} else {{
                    showLoginScreen();
                }}
            }}).catch(function(error) {{
                console.error('Auth check failed:', error);
                showLoginScreen();
            }});
            
            // Setup event listeners
            setupEventListeners();
        }}
        
        function setupEventListeners() {{
            // Login form
            document.getElementById('loginForm').addEventListener('submit', handleLogin);
            
            // Logout button
            document.getElementById('logoutBtn').addEventListener('click', handleLogout);
            
            // Sidebar toggle for mobile
            document.getElementById('sidebarToggle').addEventListener('click', toggleSidebar);
            
            // High contrast toggle
            document.getElementById('highContrastToggle').addEventListener('click', toggleHighContrast);
        }}
        
        function handleLogin(event) {{
            event.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            pywebview.api.login(username, password).then(function(response) {{
                if (response.success) {{
                    currentUser = response.user;
                    showMainApp();
                    loadDashboard();
                }} else {{
                    showAlert('loginAlert', response.message, 'danger');
                }}
            }}).catch(function(error) {{
                showAlert('loginAlert', 'Login failed. Please try again.', 'danger');
            }});
        }}
        
        function handleLogout() {{
            pywebview.api.logout().then(function() {{
                currentUser = null;
                showLoginScreen();
            }});
        }}
        
        function showLoginScreen() {{
            document.getElementById('loginScreen').classList.remove('hidden');
            document.getElementById('mainApp').classList.add('hidden');
        }}
        
        function showMainApp() {{
            document.getElementById('loginScreen').classList.add('hidden');
            document.getElementById('mainApp').classList.remove('hidden');
            updateUserInfo();
            setupSidebar();
        }}
        
        function updateUserInfo() {{
            if (currentUser) {{
                document.getElementById('userInfo').textContent = 
                    `Welcome, ${{currentUser.first_name}} ${{currentUser.last_name}}`;
            }}
        }}
        
        function setupSidebar() {{
            const sidebarNav = document.getElementById('sidebarNav');
            const navItems = getNavItems();
            
            sidebarNav.innerHTML = navItems.map(item => `
                <div class="nav-item">
                    <a href="#" class="nav-link" data-view="${{item.view}}">
                        <i class="${{item.icon}}"></i>
                        ${{item.label}}
                    </a>
                </div>
            `).join('');
            
            // Add click listeners
            sidebarNav.querySelectorAll('.nav-link').forEach(link => {{
                link.addEventListener('click', function(e) {{
                    e.preventDefault();
                    const view = this.getAttribute('data-view');
                    loadView(view);
                }});
            }});
        }}
        
        function getNavItems() {{
            const role = currentUser.role;
            const items = [];
            
            if (role === 'super_admin') {{
                items.push(
                    {{view: 'dashboard', label: 'Dashboard', icon: 'fas fa-tachometer-alt'}},
                    {{view: 'schools', label: 'Schools', icon: 'fas fa-school'}},
                    {{view: 'users', label: 'Users', icon: 'fas fa-users'}},
                    {{view: 'reports', label: 'Reports', icon: 'fas fa-chart-bar'}}
                );
            }} else if (role === 'school_admin') {{
                items.push(
                    {{view: 'dashboard', label: 'Dashboard', icon: 'fas fa-tachometer-alt'}},
                    {{view: 'classes', label: 'Classes', icon: 'fas fa-chalkboard'}},
                    {{view: 'teachers', label: 'Teachers', icon: 'fas fa-chalkboard-teacher'}},
                    {{view: 'students', label: 'Students', icon: 'fas fa-user-graduate'}},
                    {{view: 'reports', label: 'Reports', icon: 'fas fa-chart-bar'}}
                );
            }} else if (role === 'teacher') {{
                items.push(
                    {{view: 'dashboard', label: 'Dashboard', icon: 'fas fa-tachometer-alt'}},
                    {{view: 'classes', label: 'My Classes', icon: 'fas fa-chalkboard'}},
                    {{view: 'content', label: 'Content', icon: 'fas fa-book'}},
                    {{view: 'students', label: 'Students', icon: 'fas fa-user-graduate'}},
                    {{view: 'reports', label: 'Reports', icon: 'fas fa-chart-bar'}}
                );
            }} else if (role === 'student') {{
                items.push(
                    {{view: 'dashboard', label: 'Dashboard', icon: 'fas fa-tachometer-alt'}},
                    {{view: 'lessons', label: 'Lessons', icon: 'fas fa-book-open'}},
                    {{view: 'activities', label: 'Activities', icon: 'fas fa-tasks'}},
                    {{view: 'progress', label: 'Progress', icon: 'fas fa-chart-line'}}
                );
            }}
            
            return items;
        }}
        
        function loadView(view) {{
            currentView = view;
            updateActiveNav();
            updatePageTitle();
            
            switch (view) {{
                case 'dashboard':
                    loadDashboard();
                    break;
                case 'schools':
                    loadSchools();
                    break;
                case 'users':
                    loadUsers();
                    break;
                case 'classes':
                    loadClasses();
                    break;
                case 'teachers':
                    loadTeachers();
                    break;
                case 'students':
                    loadStudents();
                    break;
                case 'content':
                    loadContent();
                    break;
                case 'lessons':
                    loadLessons();
                    break;
                case 'activities':
                    loadActivities();
                    break;
                case 'progress':
                    loadProgress();
                    break;
                case 'reports':
                    loadReports();
                    break;
                default:
                    loadDashboard();
            }}
        }}
        
        function updateActiveNav() {{
            document.querySelectorAll('.nav-link').forEach(link => {{
                link.classList.remove('active');
                if (link.getAttribute('data-view') === currentView) {{
                    link.classList.add('active');
                }}
            }});
        }}
        
        function updatePageTitle() {{
            const titles = {{
                dashboard: 'Dashboard',
                schools: 'Schools',
                users: 'Users',
                classes: 'Classes',
                teachers: 'Teachers',
                students: 'Students',
                content: 'Content',
                lessons: 'Lessons',
                activities: 'Activities',
                progress: 'Progress',
                reports: 'Reports'
            }};
            
            document.getElementById('pageTitle').textContent = titles[currentView] || 'Dashboard';
        }}
        
        function loadDashboard() {{
            const contentArea = document.getElementById('contentArea');
            contentArea.innerHTML = `
                <div class="row">
                    <div class="col-md-3">
                        <div class="stat-card">
                            <div class="stat-number" id="totalSchools">-</div>
                            <div class="stat-label">Schools</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card">
                            <div class="stat-number" id="totalUsers">-</div>
                            <div class="stat-label">Users</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card">
                            <div class="stat-number" id="totalClasses">-</div>
                            <div class="stat-label">Classes</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card">
                            <div class="stat-number" id="totalStudents">-</div>
                            <div class="stat-label">Students</div>
                        </div>
                    </div>
                </div>
                <div class="dashboard-card">
                    <h5>Welcome to Mathematics Lab</h5>
                    <p>Interactive learning platform for CBSE mathematics curriculum.</p>
                </div>
            `;
            
            // Load dashboard data
            loadDashboardData();
        }}
        
        function loadDashboardData() {{
            pywebview.api.getDashboardData().then(function(data) {{
                document.getElementById('totalSchools').textContent = data.total_schools || 0;
                document.getElementById('totalUsers').textContent = data.total_users || 0;
                document.getElementById('totalClasses').textContent = data.total_classes || 0;
                document.getElementById('totalStudents').textContent = data.total_students || 0;
            }}).catch(function(error) {{
                console.error('Failed to load dashboard data:', error);
            }});
        }}
        
        function loadSchools() {{
            const contentArea = document.getElementById('contentArea');
            contentArea.innerHTML = `
                <div class="dashboard-card">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5>Schools</h5>
                        <button class="btn btn-primary" onclick="createSchool()">
                            <i class="fas fa-plus me-1"></i>Add School
                        </button>
                    </div>
                    <div id="schoolsList">Loading...</div>
                </div>
            `;
            
            pywebview.api.getSchools().then(function(schools) {{
                displaySchools(schools);
            }}).catch(function(error) {{
                document.getElementById('schoolsList').innerHTML = 
                    '<div class="alert alert-danger">Failed to load schools</div>';
            }});
        }}
        
        function displaySchools(schools) {{
            const schoolsList = document.getElementById('schoolsList');
            
            if (schools.length === 0) {{
                schoolsList.innerHTML = '<div class="alert alert-info">No schools found</div>';
                return;
            }}
            
            const table = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>City</th>
                            <th>Phone</th>
                            <th>Email</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${{schools.map(school => `
                            <tr>
                                <td>${{school.name}}</td>
                                <td>${{school.city}}</td>
                                <td>${{school.phone || '-'}}</td>
                                <td>${{school.email || '-'}}</td>
                                <td>
                                    <button class="btn btn-sm btn-outline-primary" onclick="viewSchool(${{school.id}})">
                                        <i class="fas fa-eye"></i>
                                    </button>
                                    <button class="btn btn-sm btn-outline-secondary" onclick="editSchool(${{school.id}})">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                </td>
                            </tr>
                        `).join('')}}
                    </tbody>
                </table>
            `;
            
            schoolsList.innerHTML = table;
        }}
        
        function loadUsers() {{
            const contentArea = document.getElementById('contentArea');
            contentArea.innerHTML = `
                <div class="dashboard-card">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5>Users</h5>
                        <button class="btn btn-primary" onclick="createUser()">
                            <i class="fas fa-plus me-1"></i>Add User
                        </button>
                    </div>
                    <div id="usersList">Loading...</div>
                </div>
            `;
            
            pywebview.api.getUsers().then(function(users) {{
                displayUsers(users);
            }}).catch(function(error) {{
                document.getElementById('usersList').innerHTML = 
                    '<div class="alert alert-danger">Failed to load users</div>';
            }});
        }}
        
        function displayUsers(users) {{
            const usersList = document.getElementById('usersList');
            
            if (users.length === 0) {{
                usersList.innerHTML = '<div class="alert alert-info">No users found</div>';
                return;
            }}
            
            const table = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Username</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${{users.map(user => `
                            <tr>
                                <td>${{user.first_name}} ${{user.last_name}}</td>
                                <td>${{user.username}}</td>
                                <td>${{user.email}}</td>
                                <td><span class="badge bg-primary">${{user.role}}</span></td>
                                <td>
                                    <span class="badge bg-${{user.is_active ? 'success' : 'danger'}}">
                                        ${{user.is_active ? 'Active' : 'Inactive'}}
                                    </span>
                                </td>
                                <td>
                                    <button class="btn btn-sm btn-outline-primary" onclick="viewUser(${{user.id}})">
                                        <i class="fas fa-eye"></i>
                                    </button>
                                    <button class="btn btn-sm btn-outline-secondary" onclick="editUser(${{user.id}})">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                </td>
                            </tr>
                        `).join('')}}
                    </tbody>
                </table>
            `;
            
            usersList.innerHTML = table;
        }}
        
        function loadClasses() {{
            const contentArea = document.getElementById('contentArea');
            contentArea.innerHTML = `
                <div class="dashboard-card">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5>Classes</h5>
                        <button class="btn btn-primary" onclick="createClass()">
                            <i class="fas fa-plus me-1"></i>Add Class
                        </button>
                    </div>
                    <div id="classesList">Loading...</div>
                </div>
            `;
            
            pywebview.api.getClasses().then(function(classes) {{
                displayClasses(classes);
            }}).catch(function(error) {{
                document.getElementById('classesList').innerHTML = 
                    '<div class="alert alert-danger">Failed to load classes</div>';
            }});
        }}
        
        function displayClasses(classes) {{
            const classesList = document.getElementById('classesList');
            
            if (classes.length === 0) {{
                classesList.innerHTML = '<div class="alert alert-info">No classes found</div>';
                return;
            }}
            
            const table = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>Class</th>
                            <th>Grade</th>
                            <th>Section</th>
                            <th>Teacher</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${{classes.map(cls => `
                            <tr>
                                <td>${{cls.name}}</td>
                                <td>Grade ${{cls.grade}}</td>
                                <td>${{cls.section || '-'}}</td>
                                <td>${{cls.teacher_name || 'Not Assigned'}}</td>
                                <td>
                                    <button class="btn btn-sm btn-outline-primary" onclick="viewClass(${{cls.id}})">
                                        <i class="fas fa-eye"></i>
                                    </button>
                                    <button class="btn btn-sm btn-outline-secondary" onclick="editClass(${{cls.id}})">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                </td>
                            </tr>
                        `).join('')}}
                    </tbody>
                </table>
            `;
            
            classesList.innerHTML = table;
        }}
        
        function loadTeachers() {{
            loadUsers(); // Reuse users view with teacher filter
        }}
        
        function loadStudents() {{
            loadUsers(); // Reuse users view with student filter
        }}
        
        function loadContent() {{
            const contentArea = document.getElementById('contentArea');
            contentArea.innerHTML = `
                <div class="dashboard-card">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5>Content Management</h5>
                        <button class="btn btn-primary" onclick="createContent()">
                            <i class="fas fa-plus me-1"></i>Add Content
                        </button>
                    </div>
                    <div id="contentList">Loading...</div>
                </div>
            `;
            
            pywebview.api.getContent().then(function(content) {{
                displayContent(content);
            }}).catch(function(error) {{
                document.getElementById('contentList').innerHTML = 
                    '<div class="alert alert-danger">Failed to load content</div>';
            }});
        }}
        
        function displayContent(content) {{
            const contentList = document.getElementById('contentList');
            contentList.innerHTML = '<div class="alert alert-info">Content management coming soon...</div>';
        }}
        
        function loadLessons() {{
            const contentArea = document.getElementById('contentArea');
            contentArea.innerHTML = `
                <div class="dashboard-card">
                    <h5>My Lessons</h5>
                    <div id="lessonsList">Loading...</div>
                </div>
            `;
            
            pywebview.api.getLessons().then(function(lessons) {{
                displayLessons(lessons);
            }}).catch(function(error) {{
                document.getElementById('lessonsList').innerHTML = 
                    '<div class="alert alert-danger">Failed to load lessons</div>';
            }});
        }}
        
        function displayLessons(lessons) {{
            const lessonsList = document.getElementById('lessonsList');
            lessonsList.innerHTML = '<div class="alert alert-info">Lessons coming soon...</div>';
        }}
        
        function loadActivities() {{
            const contentArea = document.getElementById('contentArea');
            contentArea.innerHTML = `
                <div class="dashboard-card">
                    <h5>My Activities</h5>
                    <div id="activitiesList">Loading...</div>
                </div>
            `;
            
            pywebview.api.getActivities().then(function(activities) {{
                displayActivities(activities);
            }}).catch(function(error) {{
                document.getElementById('activitiesList').innerHTML = 
                    '<div class="alert alert-danger">Failed to load activities</div>';
            }});
        }}
        
        function displayActivities(activities) {{
            const activitiesList = document.getElementById('activitiesList');
            activitiesList.innerHTML = '<div class="alert alert-info">Activities coming soon...</div>';
        }}
        
        function loadProgress() {{
            const contentArea = document.getElementById('contentArea');
            contentArea.innerHTML = `
                <div class="dashboard-card">
                    <h5>My Progress</h5>
                    <div id="progressContent">Loading...</div>
                </div>
            `;
            
            pywebview.api.getProgress().then(function(progress) {{
                displayProgress(progress);
            }}).catch(function(error) {{
                document.getElementById('progressContent').innerHTML = 
                    '<div class="alert alert-danger">Failed to load progress</div>';
            }});
        }}
        
        function displayProgress(progress) {{
            const progressContent = document.getElementById('progressContent');
            progressContent.innerHTML = '<div class="alert alert-info">Progress tracking coming soon...</div>';
        }}
        
        function loadReports() {{
            const contentArea = document.getElementById('contentArea');
            contentArea.innerHTML = `
                <div class="dashboard-card">
                    <h5>Reports & Analytics</h5>
                    <div id="reportsContent">Loading...</div>
                </div>
            `;
            
            pywebview.api.getReports().then(function(reports) {{
                displayReports(reports);
            }}).catch(function(error) {{
                document.getElementById('reportsContent').innerHTML = 
                    '<div class="alert alert-danger">Failed to load reports</div>';
            }});
        }}
        
        function displayReports(reports) {{
            const reportsContent = document.getElementById('reportsContent');
            reportsContent.innerHTML = '<div class="alert alert-info">Reports coming soon...</div>';
        }}
        
        function toggleSidebar() {{
            document.querySelector('.sidebar').classList.toggle('show');
        }}
        
        function toggleHighContrast() {{
            document.body.classList.toggle('high-contrast');
        }}
        
        function showAlert(elementId, message, type) {{
            const alertElement = document.getElementById(elementId);
            alertElement.className = `alert alert-${{type}}`;
            alertElement.textContent = message;
            alertElement.classList.remove('hidden');
            
            setTimeout(() => {{
                alertElement.classList.add('hidden');
            }}, 5000);
        }}
        
        // Placeholder functions for future implementation
        function createSchool() {{ alert('Create school - coming soon'); }}
        function editSchool(id) {{ alert('Edit school - coming soon'); }}
        function viewSchool(id) {{ alert('View school - coming soon'); }}
        function createUser() {{ alert('Create user - coming soon'); }}
        function editUser(id) {{ alert('Edit user - coming soon'); }}
        function viewUser(id) {{ alert('View user - coming soon'); }}
        function createClass() {{ alert('Create class - coming soon'); }}
        function editClass(id) {{ alert('Edit class - coming soon'); }}
        function viewClass(id) {{ alert('View class - coming soon'); }}
        function createContent() {{ alert('Create content - coming soon'); }}
    </script>
</body>
</html>
        """
    
    def get_js_api(self) -> object:
        """Get JavaScript API object for pywebview"""
        class JSApi:
            def __init__(self, auth_manager, db_manager):
                self.auth_manager = auth_manager
                self.db_manager = db_manager
            
            def checkAuth(self):
                """Check if user is authenticated"""
                if self.auth_manager.is_authenticated():
                    return {
                        'authenticated': True,
                        'user': self.auth_manager.get_current_user()
                    }
                return {'authenticated': False}
            
            def login(self, username, password):
                """Handle user login"""
                success, message, user = self.auth_manager.login(username, password)
                return {
                    'success': success,
                    'message': message,
                    'user': user
                }
            
            def logout(self):
                """Handle user logout"""
                return {'success': self.auth_manager.logout()}
            
            def getDashboardData(self):
                """Get dashboard statistics"""
                try:
                    schools = self.db_manager.get_schools()
                    return {
                        'total_schools': len(schools),
                        'total_users': 0,  # TODO: Implement
                        'total_classes': 0,  # TODO: Implement
                        'total_students': 0  # TODO: Implement
                    }
                except Exception as e:
                    return {'error': str(e)}
            
            def getSchools(self):
                """Get all schools"""
                try:
                    return self.db_manager.get_schools()
                except Exception as e:
                    return []
            
            def getUsers(self):
                """Get all users"""
                try:
                    # TODO: Implement get_users method in DatabaseManager
                    return []
                except Exception as e:
                    return []
            
            def getClasses(self):
                """Get classes for current user's school"""
                try:
                    user = self.auth_manager.get_current_user()
                    if user and user.get('school_id'):
                        return self.db_manager.get_classes_by_school(user['school_id'])
                    return []
                except Exception as e:
                    return []
            
            def getContent(self):
                """Get content for current user"""
                try:
                    # TODO: Implement content retrieval
                    return []
                except Exception as e:
                    return []
            
            def getLessons(self):
                """Get lessons for current user"""
                try:
                    # TODO: Implement lessons retrieval
                    return []
                except Exception as e:
                    return []
            
            def getActivities(self):
                """Get activities for current user"""
                try:
                    # TODO: Implement activities retrieval
                    return []
                except Exception as e:
                    return []
            
            def getProgress(self):
                """Get progress for current user"""
                try:
                    # TODO: Implement progress retrieval
                    return {}
                except Exception as e:
                    return {}
            
            def getReports(self):
                """Get reports for current user"""
                try:
                    # TODO: Implement reports retrieval
                    return {}
                except Exception as e:
                    return {}
        
        return JSApi(self.auth_manager, self.db_manager)