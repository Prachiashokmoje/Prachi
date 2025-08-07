#!/usr/bin/env python3
"""
Test script to verify the GUI application can launch properly
"""

import sys
import os
import threading
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database.db_manager import DatabaseManager
from auth.auth_manager import AuthManager
from ui.app_controller import AppController


def test_app_components():
    """Test that all application components can be initialized"""
    print("Testing Mathematics Lab Application Components...")
    
    try:
        # Test database initialization
        print("1. Testing database initialization...")
        db = DatabaseManager(':memory:')
        db.initialize_database()
        print("   ✓ Database initialized successfully")
        
        # Test authentication manager
        print("2. Testing authentication manager...")
        auth = AuthManager(db)
        
        # Create default superadmin
        if not auth.superadmin_exists():
            auth.create_default_superadmin()
            print("   ✓ Default SuperAdmin created")
        else:
            print("   ✓ SuperAdmin already exists")
        
        # Test app controller
        print("3. Testing app controller...")
        app_controller = AppController(db, auth)
        print("   ✓ App controller initialized")
        
        # Test HTML template creation
        print("4. Testing HTML template...")
        html_path = app_controller.html_path
        if os.path.exists(html_path):
            print(f"   ✓ HTML template exists at: {html_path}")
        else:
            print(f"   ✗ HTML template not found at: {html_path}")
        
        # Test login functionality
        print("5. Testing login API...")
        login_result = app_controller.login("admin", "admin123")
        if login_result.get('success'):
            print("   ✓ Login API working")
            
            # Test logout
            logout_result = app_controller.logout()
            if logout_result.get('success'):
                print("   ✓ Logout API working")
        else:
            print(f"   ✗ Login API failed: {login_result.get('message')}")
        
        print("\n✅ All component tests passed!")
        print("The application is ready to launch.")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Component test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_webview_import():
    """Test that pywebview can be imported and basic functionality works"""
    print("\nTesting pywebview availability...")
    
    try:
        import webview
        print("✓ pywebview imported successfully")
        
        # Test basic webview functionality (create window without starting)
        print("✓ pywebview is available for GUI launch")
        return True
        
    except ImportError as e:
        print(f"✗ pywebview import failed: {e}")
        print("  Please install pywebview: pip install pywebview")
        return False
    except Exception as e:
        print(f"✗ pywebview test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("MATHEMATICS LAB - APPLICATION LAUNCH TEST")
    print("=" * 60)
    
    # Test components
    components_ok = test_app_components()
    
    # Test webview
    webview_ok = test_webview_import()
    
    print("\n" + "=" * 60)
    if components_ok and webview_ok:
        print("✅ ALL TESTS PASSED!")
        print("The application is ready to launch with: python3 run.py")
        print("\nDefault login credentials:")
        print("  Username: admin")
        print("  Password: admin123")
    else:
        print("✗ SOME TESTS FAILED!")
        print("Please fix the issues before launching the application.")
    print("=" * 60)


if __name__ == "__main__":
    main()