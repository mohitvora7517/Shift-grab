#!/usr/bin/env python3
"""
Simple launcher for Amazon Job Monitor
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if requirements are installed."""
    try:
        import selenium
        import requests
        return True
    except ImportError:
        return False

def install_requirements():
    """Install requirements if not present."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🚀 Amazon Job Monitor Launcher")
    print("=" * 35)
    
    # Check if config exists
    if not os.path.exists("config.json"):
        print("📝 No configuration file found.")
        choice = input("Would you like to create one? (y/n): ").lower()
        if choice in ['y', 'yes']:
            print("Running configuration generator...")
            subprocess.run([sys.executable, "config_generator.py"])
        else:
            print("Please create a config.json file or run config_generator.py")
            return
    
    # Check requirements
    if not check_requirements():
        print("📦 Installing required packages...")
        if not install_requirements():
            print("❌ Failed to install requirements. Please run: pip install -r requirements.txt")
            return
    
    # Run the monitor
    print("🎯 Starting job monitor...")
    subprocess.run([sys.executable, "amazon_job_monitor.py"])

if __name__ == "__main__":
    main()