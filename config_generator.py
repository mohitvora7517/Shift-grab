#!/usr/bin/env python3
"""
Configuration Generator for Amazon Job Monitor
Interactive tool to help users create their configuration file
"""

import json
import os

def get_user_input(prompt, default=None, input_type=str):
    """Get user input with optional default value."""
    if default:
        full_prompt = f"{prompt} (default: {default}): "
    else:
        full_prompt = f"{prompt}: "
    
    while True:
        try:
            user_input = input(full_prompt).strip()
            if not user_input and default:
                return default
            elif not user_input:
                print("This field is required. Please enter a value.")
                continue
            
            if input_type == int:
                return int(user_input)
            elif input_type == bool:
                return user_input.lower() in ['true', 'yes', 'y', '1']
            else:
                return user_input
        except ValueError:
            print("Invalid input. Please try again.")

def add_job_urls():
    """Add job URLs interactively."""
    job_urls = []
    print("\n📋 Adding Job URLs")
    print("=" * 30)
    print("Enter Amazon job URLs to monitor.")
    print("You can find these by going to Amazon Jobs and copying the URL from your browser.")
    print("Example: https://hiring.amazon.ca/app#/jobDetail?jobId=JOB-CA-0000000315&locale=en-CA")
    print()
    
    while True:
        url = get_user_input("Enter job URL (or 'done' to finish)")
        if url.lower() == 'done':
            break
        if url.startswith('https://hiring.amazon.ca/'):
            job_urls.append(url)
            print(f"✅ Added: {url}")
        else:
            print("❌ Invalid URL. Please enter a valid Amazon hiring URL.")
    
    if not job_urls:
        # Add default URL
        default_url = "https://hiring.amazon.ca/app#/jobDetail?jobId=JOB-CA-0000000315&locale=en-CA"
        job_urls.append(default_url)
        print(f"📝 Added default URL: {default_url}")
    
    return job_urls

def configure_monitoring():
    """Configure monitoring settings."""
    print("\n⚙️ Monitoring Configuration")
    print("=" * 30)
    
    check_interval = get_user_input("Check interval (seconds)", "30", int)
    max_attempts = get_user_input("Maximum check attempts", "1000", int)
    headless = get_user_input("Run in headless mode (no browser window)", "true", bool)
    
    return {
        "check_interval": check_interval,
        "max_attempts": max_attempts,
        "headless": headless
    }

def configure_notifications():
    """Configure notification settings."""
    print("\n🔔 Notification Settings")
    print("=" * 30)
    
    desktop = get_user_input("Enable desktop notifications", "true", bool)
    
    email_enabled = get_user_input("Enable email notifications", "false", bool)
    email_config = {"enabled": False}
    
    if email_enabled:
        print("\n📧 Email Configuration")
        print("For Gmail, use an App Password instead of your regular password.")
        print("Enable 2FA and generate an App Password in your Google Account settings.")
        
        email_config = {
            "enabled": True,
            "smtp_server": get_user_input("SMTP server", "smtp.gmail.com"),
            "smtp_port": get_user_input("SMTP port", "587", int),
            "email": get_user_input("Your email address"),
            "password": get_user_input("Your email password/app password"),
            "to_email": get_user_input("Notification email address")
        }
    
    return {
        "desktop": desktop,
        "email": email_config
    }

def show_preview(config):
    """Show configuration preview."""
    print("\n📋 Configuration Preview")
    print("=" * 30)
    print(json.dumps(config, indent=2))
    print()

def main():
    print("🚀 Amazon Job Monitor Configuration Generator")
    print("=" * 50)
    print("This tool will help you create a configuration file for the Amazon Job Monitor.")
    print()
    
    # Get job URLs
    job_urls = add_job_urls()
    
    # Get monitoring settings
    monitoring = configure_monitoring()
    
    # Get notification settings
    notifications = configure_notifications()
    
    # Create final configuration
    config = {
        "job_urls": job_urls,
        "check_interval": monitoring["check_interval"],
        "max_attempts": monitoring["max_attempts"],
        "headless": monitoring["headless"],
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "notifications": notifications
    }
    
    # Show preview
    show_preview(config)
    
    # Confirm and save
    save = get_user_input("Save this configuration to config.json?", "true", bool)
    
    if save:
        try:
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            print("✅ Configuration saved to config.json")
            print("\n🎉 Setup complete!")
            print("You can now run: python amazon_job_monitor.py")
        except Exception as e:
            print(f"❌ Failed to save configuration: {e}")
    else:
        print("Configuration not saved.")

if __name__ == "__main__":
    main()