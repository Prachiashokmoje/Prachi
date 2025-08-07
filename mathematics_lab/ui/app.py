"""
Mathematics Lab - PyWebView Application
Main UI application using pywebview.
"""

import webview
import json
import sys
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from ..auth.authentication import auth_manager, AuthenticationError
from ..database.models import db_manager


class MathematicsLabAPI:
    """API class for Mathematics Lab application."""
    
    def __init__(self):
        self.current_user = None
        self.session_token = None
    
    def login(self, username, password):
        """Login user and return session data."""
        try:
            result = auth_manager.login(username, password)
            self.session_token = result['session_token']
            self.current_user = result['user']
            return {
                'success': True,
                'user': result['user'],
                'session_token': result['session_token']
            }
        except AuthenticationError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def logout(self):
        """Logout current user."""
        if self.session_token:
            auth_manager.logout(self.session_token)
            self.session_token = None
            self.current_user = None
        return {'success': True}
    
    def get_current_user(self):
        """Get current user information."""
        if not self.session_token:
            return {'success': False, 'error': 'Not authenticated'}
        
        try:
            user = auth_manager.get_current_user(self.session_token)
            if user:
                return {'success': True, 'user': user}
            else:
                return {'success': False, 'error': 'Session expired'}
        except AuthenticationError as e:
            return {'success': False, 'error': str(e)}
    
    def get_schools(self):
        """Get all schools (SuperAdmin only)."""
        if not self.session_token:
            return {'success': False, 'error': 'Not authenticated'}
        
        try:
            schools = auth_manager.get_schools(self.session_token)
            return {'success': True, 'schools': schools}
        except AuthenticationError as e:
            return {'success': False, 'error': str(e)}
    
    def create_school(self, name, address=None, contact_email=None, contact_phone=None):
        """Create a new school (SuperAdmin only)."""
        if not self.session_token:
            return {'success': False, 'error': 'Not authenticated'}
        
        try:
            school = auth_manager.create_school(
                self.session_token, name, address, contact_email, contact_phone
            )
            return {'success': True, 'school': school}
        except AuthenticationError as e:
            return {'success': False, 'error': str(e)}


def create_login_html():
    """Create the login page HTML."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mathematics Lab - Login</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .login-container {
                background: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 400px;
            }
            
            .login-header {
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .login-header h1 {
                color: #333;
                margin-bottom: 0.5rem;
            }
            
            .login-header p {
                color: #666;
            }
            
            .form-group {
                margin-bottom: 1rem;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 0.5rem;
                color: #333;
                font-weight: 500;
            }
            
            .form-group input {
                width: 100%;
                padding: 0.75rem;
                border: 2px solid #e1e5e9;
                border-radius: 5px;
                font-size: 1rem;
                transition: border-color 0.3s ease;
            }
            
            .form-group input:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .login-btn {
                width: 100%;
                padding: 0.75rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s ease;
            }
            
            .login-btn:hover {
                transform: translateY(-2px);
            }
            
            .error-message {
                color: #e74c3c;
                text-align: center;
                margin-top: 1rem;
                display: none;
            }
            
            .demo-credentials {
                margin-top: 1rem;
                padding: 1rem;
                background: #f8f9fa;
                border-radius: 5px;
                font-size: 0.9rem;
                color: #666;
            }
            
            .demo-credentials h4 {
                margin-bottom: 0.5rem;
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="login-header">
                <h1>Mathematics Lab</h1>
                <p>Interactive Learning Platform</p>
            </div>
            
            <form id="loginForm">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit" class="login-btn">Login</button>
            </form>
            
            <div id="errorMessage" class="error-message"></div>
            
            <div class="demo-credentials">
                <h4>Demo Credentials:</h4>
                <p><strong>SuperAdmin:</strong> superadmin / Admin123!</p>
                <p><strong>SchoolAdmin:</strong> schooladmin1 / Admin123!</p>
                <p><strong>Teacher:</strong> teacher1 / Teacher123!</p>
                <p><strong>Student:</strong> student1 / Student123!</p>
            </div>
        </div>
        
        <script>
            document.getElementById('loginForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                const errorMessage = document.getElementById('errorMessage');
                
                try {
                    const result = await pywebview.api.login(username, password);
                    
                    if (result.success) {
                        // Store session data
                        localStorage.setItem('session_token', result.session_token);
                        localStorage.setItem('user', JSON.stringify(result.user));
                        
                        // Show success message and redirect
                        alert('Login successful! Welcome, ' + result.user.first_name + ' ' + result.user.last_name);
                        
                        // In a real app, this would redirect to the main dashboard
                        // For now, just show the user info
                        document.body.innerHTML = `
                            <div style="padding: 2rem; text-align: center;">
                                <h1>Welcome, ${result.user.first_name} ${result.user.last_name}!</h1>
                                <p>Role: ${result.user.role}</p>
                                <p>School ID: ${result.user.school_id || 'N/A'}</p>
                                <button onclick="logout()" style="margin-top: 1rem; padding: 0.5rem 1rem;">Logout</button>
                            </div>
                        `;
                    } else {
                        errorMessage.textContent = result.error;
                        errorMessage.style.display = 'block';
                    }
                } catch (error) {
                    errorMessage.textContent = 'An error occurred during login.';
                    errorMessage.style.display = 'block';
                }
            });
            
            async function logout() {
                try {
                    await pywebview.api.logout();
                    localStorage.removeItem('session_token');
                    localStorage.removeItem('user');
                    location.reload();
                } catch (error) {
                    console.error('Logout error:', error);
                }
            }
        </script>
    </body>
    </html>
    """


def launch_app():
    """Launch the Mathematics Lab application."""
    # Create API instance
    api = MathematicsLabAPI()
    
    # Create the login page HTML
    html = create_login_html()
    
    # Create and start the webview window
    window = webview.create_window(
        'Mathematics Lab - Interactive Learning Platform',
        html=html,
        js_api=api,
        width=800,
        height=600,
        resizable=True,
        min_size=(600, 400)
    )
    
    # Start the application
    webview.start(debug=True)


if __name__ == "__main__":
    launch_app()