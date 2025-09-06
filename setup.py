#!/usr/bin/env python3
"""
Setup script for Amazon Job Monitor
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_chromedriver():
    """Setup ChromeDriver."""
    print("\nSetting up ChromeDriver...")
    print("Please make sure you have Google Chrome installed on your system.")
    print("ChromeDriver will be automatically managed by Selenium 4.x")
    print("✅ ChromeDriver setup complete!")

def create_config():
    """Create initial configuration."""
    print("\nCreating configuration file...")
    try:
        from amazon_job_monitor import AmazonJobMonitor
        monitor = AmazonJobMonitor()
        print("✅ Configuration file created: config.json")
        print("📝 Please edit config.json to customize your settings")
        return True
    except Exception as e:
        print(f"❌ Failed to create configuration: {e}")
        return False

def main():
    print("🚀 Amazon Job Monitor Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Setup ChromeDriver
    setup_chromedriver()
    
    # Create configuration
    if not create_config():
        return
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit config.json to add your job URLs and preferences")
    print("2. Run: python amazon_job_monitor.py")
    print("\nFor help: python amazon_job_monitor.py --help")

if __name__ == "__main__":
    main()