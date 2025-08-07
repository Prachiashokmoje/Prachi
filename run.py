#!/usr/bin/env python3
"""
Mathematics Lab - Interactive Learning Platform
Main entry point for the desktop application
"""

import sys
import os
import webview
import sqlite3
from pathlib import Path
from datetime import datetime
import hashlib
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from auth.auth_manager import AuthManager
from ui.app_ui import MathematicsLabUI

class MathematicsLabApp:
    """Main application class for Mathematics Lab"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.auth_manager = AuthManager(self.db_manager)
        self.ui = MathematicsLabUI(self.auth_manager, self.db_manager)
        self.current_user = None
        
    def initialize_database(self):
        """Initialize database with schema and sample data"""
        try:
            self.db_manager.create_tables()
            self.db_manager.create_sample_data()
            print("✅ Database initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            return False
    
    def start(self):
        """Start the Mathematics Lab application"""
        print("🚀 Starting Mathematics Lab Application...")
        
        # Initialize database
        if not self.initialize_database():
            print("Failed to initialize database. Exiting...")
            return
        
        # Create pywebview window
        window_title = "Mathematics Lab - Interactive Learning Platform"
        window_width = 1400
        window_height = 900
        
        # Create the main window
        webview.create_window(
            title=window_title,
            url=self.ui.get_main_html(),
            width=window_width,
            height=window_height,
            resizable=True,
            min_size=(1000, 700),
            text_select=True,
            confirm_close=False,
            js_api=self.ui.get_js_api()
        )
        
        # Start the application
        webview.start(debug=True)

def main():
    """Main entry point"""
    try:
        app = MathematicsLabApp()
        app.start()
    except Exception as e:
        print(f"❌ Application failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()