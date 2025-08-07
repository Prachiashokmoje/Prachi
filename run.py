#!/usr/bin/env python3
"""
Mathematics Lab - Main Application Entry Point
Initializes database and launches the pywebview application.
"""

import sys
import os
from pathlib import Path

# Add the mathematics_lab directory to the Python path
sys.path.append(str(Path(__file__).parent / "mathematics_lab"))

from mathematics_lab.database.init_db import main as init_database
from mathematics_lab.auth.session import session_manager


def main():
    """Main application entry point."""
    print("Mathematics Lab - Interactive Learning Platform")
    print("=" * 50)
    
    try:
        # Initialize database and create initial data
        print("Initializing database...")
        init_database()
        
        # Start session cleanup thread
        print("Starting session management...")
        session_manager.start_cleanup_thread()
        
        # Import and start the webview application
        print("Launching application...")
        try:
            from mathematics_lab.ui.app import launch_app
            launch_app()
        except ImportError as e:
            print(f"Import error: {e}")
            print("Please ensure all modules are properly installed.")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        session_manager.stop_cleanup_thread()
        print("Application shutdown complete.")


if __name__ == "__main__":
    main()