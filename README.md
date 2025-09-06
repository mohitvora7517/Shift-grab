# Amazon Job Application Monitor

An automated tool that monitors Amazon job postings and applies instantly when positions become available.

## Features

- 🔍 **Automatic Monitoring**: Continuously checks job availability
- ⚡ **Instant Application**: Clicks apply button the moment a job becomes active
- 🎯 **Multi-Job Support**: Monitor multiple job postings simultaneously
- 📍 **Location Flexibility**: Easy configuration for different locations and job IDs
- 🔔 **Notifications**: Desktop and email notifications when jobs become available
- 📊 **Logging**: Detailed logs of all monitoring activity
- 🛡️ **Error Handling**: Robust error handling and recovery

## Quick Start

### 1. Installation

```bash
# Clone or download the files
# Install dependencies
python setup.py
```

### 2. Configuration

Edit `config.json` to customize your settings:

```json
{
    "job_urls": [
        "https://hiring.amazon.ca/app#/jobDetail?jobId=JOB-CA-0000000315&locale=en-CA",
        "https://hiring.amazon.ca/app#/jobDetail?jobId=JOB-CA-0000000316&locale=en-CA"
    ],
    "check_interval": 30,
    "max_attempts": 1000,
    "headless": true,
    "notifications": {
        "desktop": true,
        "email": {
            "enabled": false,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "email": "your-email@gmail.com",
            "password": "your-app-password",
            "to_email": "your-email@gmail.com"
        }
    }
}
```

### 3. Run the Monitor

```bash
python amazon_job_monitor.py
```

## Configuration Options

### Job URLs
Add multiple job URLs to monitor different positions:

```json
"job_urls": [
    "https://hiring.amazon.ca/app#/jobDetail?jobId=JOB-CA-0000000315&locale=en-CA",
    "https://hiring.amazon.ca/app#/jobDetail?jobId=JOB-CA-0000000316&locale=en-CA"
]
```

### Check Interval
How often to check for job availability (in seconds):

```json
"check_interval": 30  // Check every 30 seconds
```

### Notifications

#### Desktop Notifications
```json
"notifications": {
    "desktop": true
}
```

#### Email Notifications
```json
"notifications": {
    "email": {
        "enabled": true,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "email": "your-email@gmail.com",
        "password": "your-app-password",
        "to_email": "your-email@gmail.com"
    }
}
```

## Finding Job URLs

1. Go to [Amazon Jobs](https://hiring.amazon.ca/)
2. Search for warehouse positions in your desired location
3. Click on a job posting
4. Copy the URL from your browser
5. Add it to your `config.json` file

## Different Locations

To monitor jobs in different locations:

1. **Toronto**: `https://hiring.amazon.ca/app#/jobDetail?jobId=JOB-CA-0000000315&locale=en-CA`
2. **Vancouver**: Search for Vancouver jobs and copy the URL
3. **Montreal**: Search for Montreal jobs and copy the URL
4. **Calgary**: Search for Calgary jobs and copy the URL

Simply replace the job ID in the URL to monitor different positions in the same location.

## Usage Examples

### Basic Usage
```bash
python amazon_job_monitor.py
```

### Custom Config File
```bash
python amazon_job_monitor.py --config my_config.json
```

### Setup Mode
```bash
python amazon_job_monitor.py --setup
```

## Troubleshooting

### Chrome/ChromeDriver Issues
- Make sure Google Chrome is installed
- The script uses Selenium 4.x which manages ChromeDriver automatically
- If you encounter issues, try running with `"headless": false` to see what's happening

### Permission Issues
- Make sure you have write permissions in the directory
- The script creates log files and configuration files

### Network Issues
- Check your internet connection
- Amazon's website might be temporarily unavailable

## Logs

The script creates detailed logs in `amazon_job_monitor.log`:

```
2024-01-15 10:30:15 - INFO - Starting Amazon Job Monitor...
2024-01-15 10:30:15 - INFO - Monitoring 2 job(s)
2024-01-15 10:30:15 - INFO - Check interval: 30 seconds
2024-01-15 10:30:16 - INFO - Check attempt #1
2024-01-15 10:30:16 - INFO - Checking job 1/2
2024-01-15 10:30:19 - INFO - Job not available: No work shift found
```

## Legal Notice

This tool is for educational and personal use only. Please ensure you comply with Amazon's terms of service and use responsibly. The tool should not be used to spam or abuse their systems.

## Support

If you encounter any issues:

1. Check the logs in `amazon_job_monitor.log`
2. Verify your configuration in `config.json`
3. Make sure all dependencies are installed
4. Ensure you have a stable internet connection

## Requirements

- Python 3.7+
- Google Chrome browser
- Internet connection
- Required Python packages (installed via setup.py)