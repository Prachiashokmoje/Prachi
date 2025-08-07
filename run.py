#!/usr/bin/env python3
"""
Mathematics Lab Application - Main Entry Point
A comprehensive mathematics learning platform with role-based access
"""

import sys
import os
import webview
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database.db_manager import DatabaseManager
from src.auth.auth_manager import AuthManager
from src.ui.app_controller import AppController


def main():
    """Initialize the application and launch the GUI"""
    try:
        # Initialize database
        print("Initializing Mathematics Lab...")
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        
        # Initialize authentication
        auth_manager = AuthManager(db_manager)
        
        # Create app controller
        app_controller = AppController(db_manager, auth_manager)
        
        # Create default superadmin if none exists
        if not auth_manager.superadmin_exists():
            print("Creating default SuperAdmin account...")
            auth_manager.create_default_superadmin()
            print("Default SuperAdmin created: username='admin', password='admin123'")
        
        # Launch the application
        print("Launching Mathematics Lab application...")
        webview.create_window(
            title="Mathematics Lab",
            js_api=app_controller,
            url=app_controller.html_path,
            width=1200,
            height=800,
            min_size=(800, 600),
            resizable=True
        )
        
        webview.start(debug=False)
        
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()