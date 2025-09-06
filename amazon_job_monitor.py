#!/usr/bin/env python3
"""
Amazon Job Application Monitor
Automatically monitors Amazon job postings and applies when they become active.
"""

import time
import json
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
from datetime import datetime
import argparse

class AmazonJobMonitor:
    def __init__(self, config_file="config.json"):
        """Initialize the job monitor with configuration."""
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.driver = None
        
    def load_config(self, config_file):
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default config if file doesn't exist
            default_config = {
                "job_urls": [
                    "https://hiring.amazon.ca/app#/jobDetail?jobId=JOB-CA-0000000315&locale=en-CA"
                ],
                "check_interval": 30,  # seconds
                "max_attempts": 1000,
                "headless": True,
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "notifications": {
                    "email": {
                        "enabled": False,
                        "smtp_server": "smtp.gmail.com",
                        "smtp_port": 587,
                        "email": "",
                        "password": "",
                        "to_email": ""
                    },
                    "desktop": True
                }
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            print(f"Created default config file: {config_file}")
            return default_config
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('amazon_job_monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        
        if self.config.get("headless", True):
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"--user-agent={self.config.get('user_agent', '')}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Reduce warnings and improve performance
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--log-level=3")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup Chrome driver: {e}")
            return False
    
    def check_job_availability(self, job_url):
        """Check if a job is available for application."""
        try:
            self.driver.get(job_url)
            time.sleep(3)  # Wait for page to load
            
            # Check for the warning banner that indicates job is not available
            try:
                warning_banner = self.driver.find_element(By.XPATH, "//*[contains(text(), 'This job is not available for application now')]")
                if warning_banner.is_displayed():
                    return False, "Job not available - warning banner present"
            except NoSuchElementException:
                pass
            
            # Check for "No work shift found" message
            try:
                no_shift = self.driver.find_element(By.XPATH, "//*[contains(text(), 'No work shift found')]")
                if no_shift.is_displayed():
                    return False, "No work shift found"
            except NoSuchElementException:
                pass
            
            # Check if Apply button is enabled
            try:
                apply_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Apply')]"))
                )
                
                # Check if button is enabled (not greyed out)
                if apply_button.is_enabled() and "disabled" not in apply_button.get_attribute("class"):
                    return True, "Apply button is active"
                else:
                    return False, "Apply button is disabled"
                    
            except TimeoutException:
                return False, "Apply button not found"
                
        except Exception as e:
            self.logger.error(f"Error checking job availability: {e}")
            return False, f"Error: {str(e)}"
    
    def apply_for_job(self, job_url):
        """Attempt to apply for the job."""
        try:
            self.driver.get(job_url)
            time.sleep(3)
            
            # Click the Apply button
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply')]"))
            )
            apply_button.click()
            
            self.logger.info("Successfully clicked Apply button!")
            
            # Wait a moment to see if any additional steps are required
            time.sleep(5)
            
            # Check if we're redirected to an application form
            current_url = self.driver.current_url
            if "application" in current_url.lower() or "apply" in current_url.lower():
                self.logger.info("Redirected to application form")
                return True, "Application process started"
            else:
                return True, "Apply button clicked successfully"
                
        except Exception as e:
            self.logger.error(f"Error applying for job: {e}")
            return False, f"Error: {str(e)}"
    
    def send_notification(self, message, job_url):
        """Send notification about job status."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}\nJob URL: {job_url}"
        
        self.logger.info(f"NOTIFICATION: {message}")
        
        # Desktop notification
        if self.config.get("notifications", {}).get("desktop", True):
            try:
                import plyer
                plyer.notification.notify(
                    title="Amazon Job Monitor",
                    message=message,
                    timeout=10
                )
            except ImportError:
                self.logger.warning("plyer not installed - desktop notifications disabled")
            except Exception as e:
                self.logger.warning(f"Desktop notification failed: {e}")
        
        # Email notification (if configured)
        email_config = self.config.get("notifications", {}).get("email", {})
        if email_config.get("enabled", False):
            self.send_email_notification(full_message, email_config)
    
    def send_email_notification(self, message, email_config):
        """Send email notification."""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart()
            msg['From'] = email_config['email']
            msg['To'] = email_config['to_email']
            msg['Subject'] = "Amazon Job Monitor Alert"
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['email'], email_config['password'])
            text = msg.as_string()
            server.sendmail(email_config['email'], email_config['to_email'], text)
            server.quit()
            
            self.logger.info("Email notification sent successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to send email notification: {e}")
    
    def monitor_jobs(self):
        """Main monitoring loop."""
        self.logger.info("Starting Amazon Job Monitor...")
        self.logger.info(f"Monitoring {len(self.config['job_urls'])} job(s)")
        self.logger.info(f"Check interval: {self.config['check_interval']} seconds")
        
        if not self.setup_driver():
            self.logger.error("Failed to setup WebDriver. Exiting.")
            return
        
        try:
            attempt = 0
            while attempt < self.config.get("max_attempts", 1000):
                attempt += 1
                self.logger.info(f"Check attempt #{attempt}")
                
                for i, job_url in enumerate(self.config['job_urls']):
                    self.logger.info(f"Checking job {i+1}/{len(self.config['job_urls'])}")
                    
                    is_available, status = self.check_job_availability(job_url)
                    
                    if is_available:
                        self.logger.info(f"🎉 JOB IS AVAILABLE! Status: {status}")
                        self.send_notification(f"Job is now available! Status: {status}", job_url)
                        
                        # Attempt to apply
                        success, result = self.apply_for_job(job_url)
                        if success:
                            self.send_notification(f"Successfully applied! {result}", job_url)
                            self.logger.info("Application submitted successfully!")
                        else:
                            self.send_notification(f"Failed to apply: {result}", job_url)
                            self.logger.error(f"Failed to apply: {result}")
                        
                        # Wait before checking again
                        time.sleep(60)
                    else:
                        self.logger.info(f"Job not available: {status}")
                
                # Wait before next check
                self.logger.info(f"Waiting {self.config['check_interval']} seconds before next check...")
                time.sleep(self.config['check_interval'])
                
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("WebDriver closed")

def main():
    parser = argparse.ArgumentParser(description="Amazon Job Application Monitor")
    parser.add_argument("--config", default="config.json", help="Configuration file path")
    parser.add_argument("--setup", action="store_true", help="Setup configuration file")
    args = parser.parse_args()
    
    if args.setup:
        print("Setting up configuration...")
        monitor = AmazonJobMonitor(args.config)
        print(f"Configuration file created: {args.config}")
        print("Please edit the configuration file with your settings before running the monitor.")
        return
    
    monitor = AmazonJobMonitor(args.config)
    monitor.monitor_jobs()

if __name__ == "__main__":
    main()