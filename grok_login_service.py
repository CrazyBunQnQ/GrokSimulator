from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

app = Flask(__name__)

def log_page_content(driver, step_name):
    with open('login_log.txt', 'a') as f:
        f.write(f"Step: {step_name}\n")
        f.write(driver.page_source)
        f.write("\n\n")

def simulate_login():
    load_dotenv()
    username = os.getenv('X_USERNAME')
    password = os.getenv('X_PASSWORD')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Step 1: Navigate to login page
        driver.get('https://x.com/i/grok')
        log_page_content(driver, 'Initial Page Load')
        
        # Wait for page to fully load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        
        # Step 2: Input username
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"], input[name="text"]'))
            )
            username_field.send_keys(username)
            log_page_content(driver, 'After Username Input')
        except Exception as e:
            log_page_content(driver, f'Error finding username field: {str(e)}')
            raise
        
        # Step 3: Click Next button
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Next")]'))
            )
            next_button.click()
            log_page_content(driver, 'After Clicking Next')
        except Exception as e:
            log_page_content(driver, f'Error clicking Next button: {str(e)}')
            raise
        
        # Step 4: Input password
        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="current-password"], input[name="password"]'))
            )
            password_field.send_keys(password)
            log_page_content(driver, 'After Password Input')
        except Exception as e:
            log_page_content(driver, f'Error finding password field: {str(e)}')
            raise
        
        # Step 5: Click Login button
        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Log in")]'))
            )
            login_button.click()
            log_page_content(driver, 'After Clicking Login')
        except Exception as e:
            log_page_content(driver, f'Error clicking Login button: {str(e)}')
            raise
        
        # Step 6: Get logged-in username
        try:
            logged_in_username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="UserAvatar-Container"], div[aria-label="Account menu"]'))
            ).text
            log_page_content(driver, 'After Successful Login')
            return logged_in_username
        except Exception as e:
            log_page_content(driver, f'Error finding logged-in username: {str(e)}')
            raise
        
    except Exception as e:
        log_page_content(driver, f'Login failed: {str(e)}')
        raise
    finally:
        driver.quit()

@app.route('/login', methods=['POST'])
def login():
    try:
        username = simulate_login()
        return f'Successfully logged in as: {username}'
    except Exception as e:
        return f'Login failed: {str(e)}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51776)