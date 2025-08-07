import webview
from app import create_app
import os
import sys

def main():
    """Main entry point for the Mathematics Lab application"""
    
    # Create Flask application
    app = create_app()
    
    # Set up PyWebView window
    window_title = "Mathematics Lab - Interactive Learning Platform"
    window_width = 1200
    window_height = 800
    
    # Create PyWebView window
    webview.create_window(
        title=window_title,
        url=app,
        width=window_width,
        height=window_height,
        resizable=True,
        min_size=(800, 600),
        text_select=True,
        confirm_close=False
    )
    
    # Start the application
    webview.start(debug=True)

if __name__ == "__main__":
    main()