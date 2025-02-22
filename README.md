# Grok Simulator

This project simulates login to https://x.com/i/grok using Selenium and provides a web service interface.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the service:
   ```bash
   python3 grok_login_service.py
   ```

3. The service will be available at http://localhost:51776

## Usage

To trigger the login simulation, send a POST request to:
```
POST http://localhost:51776/login
```

## Requirements

- Python 3.8+
- ChromeDriver
# GrokSimulator

## Logging

Logs are stored in `login_log.txt` by default. This file is ignored by `.gitignore` to prevent sensitive information from being committed to the repository.
