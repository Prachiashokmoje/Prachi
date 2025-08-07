"""
App Controller for Mathematics Lab Application
Serves as the API bridge between pywebview frontend and backend
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from database.db_manager import DatabaseManager
from auth.auth_manager import AuthManager


class AppController:
    """Main controller for the Mathematics Lab application"""
    
    def __init__(self, db_manager: DatabaseManager, auth_manager: AuthManager):
        """Initialize app controller"""
        self.db = db_manager
        self.auth = auth_manager
        self.current_session = None
        self.html_path = self._get_html_path()
    
    def _get_html_path(self) -> str:
        """Get the path to the HTML file"""
        ui_dir = Path(__file__).parent
        html_file = ui_dir / "templates" / "index.html"
        
        if not html_file.exists():
            # Create basic HTML if it doesn't exist
            self._create_basic_html(html_file)
        
        return str(html_file)
    
    def _create_basic_html(self, html_file: Path):
        """Create basic HTML template"""
        html_file.parent.mkdir(exist_ok=True)
        
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mathematics Lab</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            width: 100%;
            max-width: 1200px;
            height: 90vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: #4a5568;
            color: white;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            font-size: 1.5rem;
            font-weight: 600;
        }
        
        .main-content {
            flex: 1;
            display: flex;
            overflow: hidden;
        }
        
        .sidebar {
            width: 250px;
            background: #f7fafc;
            border-right: 1px solid #e2e8f0;
            padding: 1rem;
            overflow-y: auto;
        }
        
        .content-area {
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
        }
        
        .login-form {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #4a5568;
        }
        
        .form-group input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #e2e8f0;
            border-radius: 5px;
            font-size: 1rem;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            transition: background 0.2s;
        }
        
        .btn:hover {
            background: #5a67d8;
        }
        
        .btn-full {
            width: 100%;
        }
        
        .error-message {
            color: #e53e3e;
            margin-top: 0.5rem;
            font-size: 0.875rem;
        }
        
        .success-message {
            color: #38a169;
            margin-top: 0.5rem;
            font-size: 0.875rem;
        }
        
        .hidden {
            display: none;
        }
        
        .nav-item {
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.2s;
        }
        
        .nav-item:hover {
            background: #e2e8f0;
        }
        
        .nav-item.active {
            background: #667eea;
            color: white;
        }
        
        .card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #2d3748;
        }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .user-avatar {
            width: 40px;
            height: 40px;
            background: #667eea;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }
        
        .logout-btn {
            background: #e53e3e;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.875rem;
        }
        
        .logout-btn:hover {
            background: #c53030;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Login Screen -->
        <div id="loginScreen" class="login-form">
            <h2 style="text-align: center; margin-bottom: 2rem; color: #4a5568;">Mathematics Lab</h2>
            <form id="loginForm">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="btn btn-full">Login</button>
                <div id="loginError" class="error-message hidden"></div>
            </form>
            <div style="text-align: center; margin-top: 2rem; color: #718096; font-size: 0.875rem;">
                Default SuperAdmin: admin / admin123
            </div>
        </div>
        
        <!-- Main Application -->
        <div id="mainApp" class="hidden">
            <div class="header">
                <h1>Mathematics Lab</h1>
                <div class="user-info">
                    <div class="user-avatar" id="userAvatar"></div>
                    <div>
                        <div id="userName" style="font-weight: 600;"></div>
                        <div id="userRole" style="font-size: 0.875rem; opacity: 0.8;"></div>
                    </div>
                    <button class="logout-btn" onclick="logout()">Logout</button>
                </div>
            </div>
            
            <div class="main-content">
                <div class="sidebar">
                    <div id="navigation"></div>
                </div>
                
                <div class="content-area">
                    <div id="contentArea">
                        <div class="card">
                            <div class="card-title">Welcome to Mathematics Lab</div>
                            <p>Select an option from the sidebar to get started.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentUser = null;
        
        // Initialize the application
        document.addEventListener('DOMContentLoaded', function() {
            // Check if user is already logged in
            checkSession();
            
            // Set up login form
            document.getElementById('loginForm').addEventListener('submit', handleLogin);
        });
        
        async function checkSession() {
            try {
                const user = await pywebview.api.get_current_user();
                if (user) {
                    currentUser = user;
                    showMainApp();
                }
            } catch (error) {
                console.log('No active session');
            }
        }
        
        async function handleLogin(event) {
            event.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('loginError');
            
            try {
                const result = await pywebview.api.login(username, password);
                
                if (result.success) {
                    currentUser = result.user;
                    showMainApp();
                } else {
                    errorDiv.textContent = result.message || 'Login failed';
                    errorDiv.classList.remove('hidden');
                }
            } catch (error) {
                errorDiv.textContent = 'An error occurred during login';
                errorDiv.classList.remove('hidden');
            }
        }
        
        function showMainApp() {
            document.getElementById('loginScreen').classList.add('hidden');
            document.getElementById('mainApp').classList.remove('hidden');
            
            // Update user info
            const userName = `${currentUser.first_name || ''} ${currentUser.last_name || ''}`.trim() || currentUser.username;
            document.getElementById('userName').textContent = userName;
            document.getElementById('userRole').textContent = currentUser.role;
            document.getElementById('userAvatar').textContent = userName.charAt(0).toUpperCase();
            
            // Build navigation based on user role
            buildNavigation();
        }
        
        function buildNavigation() {
            const nav = document.getElementById('navigation');
            const items = [];
            
            // Common items
            items.push({ id: 'dashboard', text: 'Dashboard', icon: '📊' });
            
            // Role-specific items
            switch (currentUser.role) {
                case 'SuperAdmin':
                    items.push({ id: 'schools', text: 'Manage Schools', icon: '🏫' });
                    items.push({ id: 'users', text: 'Manage Users', icon: '👥' });
                    break;
                    
                case 'SchoolAdmin':
                    items.push({ id: 'classes', text: 'Manage Classes', icon: '📚' });
                    items.push({ id: 'teachers', text: 'Manage Teachers', icon: '👨‍🏫' });
                    items.push({ id: 'students', text: 'Manage Students', icon: '👨‍🎓' });
                    items.push({ id: 'syllabus', text: 'CBSE Syllabus', icon: '📋' });
                    break;
                    
                case 'Teacher':
                    items.push({ id: 'my-classes', text: 'My Classes', icon: '📚' });
                    items.push({ id: 'lessons', text: 'Lessons', icon: '📖' });
                    items.push({ id: 'activities', text: 'Activities', icon: '🎯' });
                    items.push({ id: 'analytics', text: 'Analytics', icon: '📈' });
                    break;
                    
                case 'Student':
                    items.push({ id: 'my-syllabus', text: 'My Syllabus', icon: '📋' });
                    items.push({ id: 'lessons', text: 'Lessons', icon: '📖' });
                    items.push({ id: 'activities', text: 'Activities', icon: '🎯' });
                    items.push({ id: 'progress', text: 'My Progress', icon: '📈' });
                    break;
            }
            
            // Profile and settings
            items.push({ id: 'profile', text: 'Profile', icon: '👤' });
            
            // Build navigation HTML
            nav.innerHTML = items.map(item => 
                `<div class="nav-item" onclick="navigateTo('${item.id}')">
                    ${item.icon} ${item.text}
                </div>`
            ).join('');
        }
        
        async function navigateTo(section) {
            // Update active navigation
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Load content
            const contentArea = document.getElementById('contentArea');
            
            try {
                const content = await pywebview.api.get_page_content(section);
                contentArea.innerHTML = content;
            } catch (error) {
                contentArea.innerHTML = `
                    <div class="card">
                        <div class="card-title">Error</div>
                        <p>Failed to load content: ${error.message}</p>
                    </div>
                `;
            }
        }
        
        async function logout() {
            try {
                await pywebview.api.logout();
                currentUser = null;
                
                // Reset form
                document.getElementById('loginForm').reset();
                document.getElementById('loginError').classList.add('hidden');
                
                // Show login screen
                document.getElementById('mainApp').classList.add('hidden');
                document.getElementById('loginScreen').classList.remove('hidden');
            } catch (error) {
                console.error('Logout error:', error);
            }
        }
    </script>
</body>
</html>'''
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    # API Methods exposed to JavaScript
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Handle user login"""
        try:
            user = self.auth.authenticate_user(username, password)
            if user:
                session_id = self.auth.create_session(user['id'])
                self.current_session = {
                    'session_id': session_id,
                    'user': user
                }
                return {
                    'success': True,
                    'user': user,
                    'session_id': session_id
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid username or password'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Login error: {str(e)}'
            }
    
    def logout(self) -> Dict[str, Any]:
        """Handle user logout"""
        try:
            if self.current_session and self.current_session.get('session_id'):
                self.auth.invalidate_session(self.current_session['session_id'])
            
            self.current_session = None
            return {'success': True}
        except Exception as e:
            return {
                'success': False,
                'message': f'Logout error: {str(e)}'
            }
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current logged-in user"""
        if self.current_session and self.current_session.get('user'):
            # Validate session is still active
            session_id = self.current_session.get('session_id')
            if session_id:
                validated_session = self.auth.validate_session(session_id)
                if validated_session:
                    return self.current_session['user']
                else:
                    self.current_session = None
        
        return None
    
    def get_page_content(self, section: str) -> str:
        """Get content for a specific page section"""
        user = self.get_current_user()
        if not user:
            return '<div class="card"><div class="card-title">Authentication Required</div><p>Please log in to access this content.</p></div>'
        
        try:
            # Route to appropriate content based on section and user role
            if section == 'dashboard':
                return self._get_dashboard_content(user)
            elif section == 'schools' and user['role'] == 'SuperAdmin':
                return self._get_schools_content()
            elif section == 'users' and user['role'] == 'SuperAdmin':
                return self._get_users_content()
            elif section == 'profile':
                return self._get_profile_content(user)
            else:
                return f'<div class="card"><div class="card-title">{section.replace("-", " ").title()}</div><p>This feature is under development.</p></div>'
        
        except Exception as e:
            return f'<div class="card"><div class="card-title">Error</div><p>Failed to load content: {str(e)}</p></div>'
    
    def _get_dashboard_content(self, user: Dict[str, Any]) -> str:
        """Get dashboard content based on user role"""
        role = user['role']
        
        if role == 'SuperAdmin':
            schools_count = len(self.db.get_schools())
            users_query = "SELECT COUNT(*) as count FROM users WHERE is_active = 1"
            users_count = self.db.execute_query(users_query)[0]['count']
            
            return f'''
            <div class="card">
                <div class="card-title">SuperAdmin Dashboard</div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
                    <div style="background: #667eea; color: white; padding: 1.5rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem; font-weight: bold;">{schools_count}</div>
                        <div>Schools</div>
                    </div>
                    <div style="background: #48bb78; color: white; padding: 1.5rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 2rem; font-weight: bold;">{users_count}</div>
                        <div>Total Users</div>
                    </div>
                </div>
                <p style="margin-top: 1rem;">Welcome to the Mathematics Lab administration panel. Use the sidebar to manage schools and users.</p>
            </div>
            '''
        
        elif role == 'SchoolAdmin':
            school_id = user['school_id']
            school = self.db.get_school_by_id(school_id) if school_id else None
            school_name = school['name'] if school else 'Unknown School'
            
            return f'''
            <div class="card">
                <div class="card-title">School Admin Dashboard</div>
                <p><strong>School:</strong> {school_name}</p>
                <p style="margin-top: 1rem;">Manage your school's classes, teachers, and students using the sidebar navigation.</p>
            </div>
            '''
        
        elif role == 'Teacher':
            return '''
            <div class="card">
                <div class="card-title">Teacher Dashboard</div>
                <p>Welcome to your teaching dashboard. Here you can manage your classes, create lessons and activities, and track student progress.</p>
            </div>
            '''
        
        elif role == 'Student':
            return '''
            <div class="card">
                <div class="card-title">Student Dashboard</div>
                <p>Welcome to your learning dashboard. Access your syllabus, lessons, and activities to enhance your mathematics skills.</p>
            </div>
            '''
        
        return '<div class="card"><div class="card-title">Dashboard</div><p>Welcome to Mathematics Lab!</p></div>'
    
    def _get_schools_content(self) -> str:
        """Get schools management content"""
        schools = self.db.get_schools()
        
        schools_html = ''
        for school in schools:
            schools_html += f'''
            <tr>
                <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0;">{school['name']}</td>
                <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0;">{school['contact_email'] or 'N/A'}</td>
                <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0;">{school['contact_phone'] or 'N/A'}</td>
                <td style="padding: 0.75rem; border-bottom: 1px solid #e2e8f0;">
                    <button class="btn" style="background: #48bb78; padding: 0.25rem 0.5rem; font-size: 0.875rem;">Edit</button>
                </td>
            </tr>
            '''
        
        return f'''
        <div class="card">
            <div class="card-title">Manage Schools</div>
            <button class="btn" style="margin-bottom: 1rem;">Add New School</button>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: #f7fafc;">
                        <th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid #e2e8f0;">School Name</th>
                        <th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid #e2e8f0;">Email</th>
                        <th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid #e2e8f0;">Phone</th>
                        <th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid #e2e8f0;">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {schools_html}
                </tbody>
            </table>
        </div>
        '''
    
    def _get_users_content(self) -> str:
        """Get users management content"""
        # Get users by role
        superadmins = self.auth.get_users_by_role('SuperAdmin')
        school_admins = self.auth.get_users_by_role('SchoolAdmin')
        
        return '''
        <div class="card">
            <div class="card-title">Manage Users</div>
            <button class="btn" style="margin-bottom: 1rem;">Add New User</button>
            <p>User management features are under development. Currently showing active user counts by role.</p>
            <div style="margin-top: 1rem;">
                <p><strong>SuperAdmins:</strong> {}</p>
                <p><strong>School Admins:</strong> {}</p>
            </div>
        </div>
        '''.format(len(superadmins), len(school_admins))
    
    def _get_profile_content(self, user: Dict[str, Any]) -> str:
        """Get user profile content"""
        return f'''
        <div class="card">
            <div class="card-title">User Profile</div>
            <div style="display: grid; grid-template-columns: 200px 1fr; gap: 1rem; margin-top: 1rem;">
                <div style="text-align: center;">
                    <div style="width: 120px; height: 120px; background: #667eea; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem; font-weight: bold; margin: 0 auto 1rem;">
                        {user['username'][0].upper()}
                    </div>
                </div>
                <div>
                    <div class="form-group">
                        <label>Username</label>
                        <input type="text" value="{user['username']}" readonly style="background: #f7fafc;">
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" value="{user['email']}" readonly style="background: #f7fafc;">
                    </div>
                    <div class="form-group">
                        <label>Role</label>
                        <input type="text" value="{user['role']}" readonly style="background: #f7fafc;">
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div class="form-group">
                            <label>First Name</label>
                            <input type="text" value="{user['first_name'] or ''}" readonly style="background: #f7fafc;">
                        </div>
                        <div class="form-group">
                            <label>Last Name</label>
                            <input type="text" value="{user['last_name'] or ''}" readonly style="background: #f7fafc;">
                        </div>
                    </div>
                </div>
            </div>
            <div style="margin-top: 2rem;">
                <button class="btn" style="background: #48bb78;">Edit Profile</button>
                <button class="btn" style="background: #ed8936; margin-left: 0.5rem;">Change Password</button>
            </div>
        </div>
        '''