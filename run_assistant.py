#!/usr/bin/env python3
"""
Python Assistant Launcher
This script sets up and runs the Python Assistant web application
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'pandas', 'numpy', 'matplotlib', 
        'seaborn', 'scikit-learn', 'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages)
            print("Packages installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error installing packages: {e}")
            return False
    
    return True

def setup_environment():
    """Set up the environment for the Python Assistant"""
    print("Setting up Python Assistant environment...")
    
    # Create necessary directories
    directories = [
        'templates', 'static/css', 'static/js', 
        'example_notebooks', 'data', 'models'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")
    
    print("Environment setup complete!")

def run_assistant():
    """Run the Python Assistant web application"""
    print("Starting Python Assistant...")
    print("The assistant will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the assistant")
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nPython Assistant stopped.")
    except Exception as e:
        print(f"Error running Python Assistant: {e}")

def main():
    """Main function"""
    print("=" * 50)
    print("🐍 PYTHON ASSISTANT")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("Failed to install required dependencies. Exiting.")
        return
    
    # Setup environment
    setup_environment()
    
    # Run the assistant
    run_assistant()

if __name__ == "__main__":
    main()