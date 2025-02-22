import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time
import logging

# Configure logging
logging.basicConfig(
    filename='login_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_page_content(driver):
    """Get and log the current page content"""
    content = driver.page_source
    logging.info(f"Page Content:\n{content}")
    return content

def login_to_grok():
    try:
        # Load environment variables with detailed logging
        load_dotenv()
        logging.info("Loading environment variables")
        username = os.getenv('X_USERNAME')
        password = os.getenv('X_PASSWORD')
        logging.info(f"Username: {'*' * len(username) if username else 'Not found'}")
        logging.info(f"Password: {'*' * len(password) if password else 'Not found'}")

        if not username or not password:
            raise ValueError("Username or password not found in .env file")
        
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')  # Run in headless mode

        # Verify ChromeDriver installation
        logging.info("Checking ChromeDriver installation")
        try:
            logging.info("Initializing ChromeDriver with options: %s", options.arguments)
            test_driver = webdriver.Chrome(options=options)
            logging.info("ChromeDriver initialized successfully")
            test_driver.quit()
            logging.info("Test ChromeDriver session closed")
        except WebDriverException as e:
            logging.error("ChromeDriver initialization failed with WebDriverException")
            logging.error("Error details: %s", str(e))
            logging.error("Stacktrace: %s", e.stacktrace)
            raise
        except Exception as e:
            logging.error("ChromeDriver initialization failed with unexpected error")
            logging.error("Error details: %s", str(e))
            raise

        # Initialize WebDriver
        driver = webdriver.Chrome(options=options)
        driver.get('https://x.com/i/grok')

        # Wait for login page to load and log initial content
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        get_page_content(driver)

        # Enter username
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
        )
        username_field.send_keys(username)
        get_page_content(driver)

        # Click Next button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Next")]'))
        )
        next_button.click()
        get_page_content(driver)

        # Enter password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="current-password"]'))
        )
        password_field.send_keys(password)
        get_page_content(driver)

        # Click Login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Log in")]'))
        )
        login_button.click()
        get_page_content(driver)

        # Wait for login to complete and get user name
        user_name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="User-Name"]'))
        )
        user_name = user_name_element.text
        logging.info(f"Successfully logged in as: {user_name}")

        return user_name

    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        raise
    finally:
        driver.quit()

if __name__ == '__main__':
    try:
        user_name = login_to_grok()
        print(f"Logged in as: {user_name}")
    except Exception as e:
        print(f"Login failed: {str(e)}")