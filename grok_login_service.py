import os
import json
import requests
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

def get_cookies_from_cloud():
    """Fetch cookies from CookieCloud service and extract essential x.com cookies"""
    load_dotenv()
    cookie_url = os.getenv('COOKIE_URL')
    cookie_uid = os.getenv('COOKIE_UID')
    cookie_pwd = os.getenv('COOKIE_PWD')
    
    if not all([cookie_url, cookie_uid, cookie_pwd]):
        raise ValueError("Missing required CookieCloud configuration in .env file")
    
    url = f"{cookie_url}/get/{cookie_uid}"
    try:
        response = requests.post(url, data={'password': cookie_pwd})
        response.raise_for_status()
        cookies_data = response.json()
        all_cookies = cookies_data.get('cookie_data', {}).get('x.com', [])
        
        # Extract essential cookies for x.com authentication
        essential_cookies = [
            cookie for cookie in all_cookies 
            if cookie['name'] in ['guest_id', 'auth_token', 'ct0', 'kdt']
        ]
        
        if not essential_cookies:
            raise ValueError("No essential x.com cookies found in CookieCloud response")
            
        return essential_cookies
    except Exception as e:
        logging.error(f"Failed to fetch cookies from CookieCloud: {str(e)}")
        raise

def save_cookies(cookies, path='x.cookie'):
    """Save cookies to file"""
    try:
        with open(path, 'w') as f:
            json.dump(cookies, f)
        logging.info(f"Cookies saved to {path}")
    except Exception as e:
        logging.error(f"Failed to save cookies: {str(e)}")
        raise

def load_cookies(path='x.cookie'):
    """Load cookies from file and validate essential x.com cookies"""
    try:
        with open(path, 'r') as f:
            cookies = json.load(f)
            
            # Validate that essential cookies are present
            essential_names = {'guest_id', 'auth_token', 'ct0', 'kdt'}
            present_names = {cookie['name'] for cookie in cookies}
            
            if not essential_names.issubset(present_names):
                logging.warning("Essential cookies missing in file, will fetch new ones")
                return None
                
            return cookies
    except FileNotFoundError:
        logging.info(f"No cookie file found at {path}")
        return None
    except Exception as e:
        logging.error(f"Failed to load cookies: {str(e)}")
        return None

def login_to_grok():
    driver = None
    try:
        # Load environment variables
        load_dotenv()
        logging.info("Loading environment variables")
        
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        
        # Initialize WebDriver
        driver = webdriver.Chrome(options=options)
        
        # Try to load existing cookies
        cookies = load_cookies()
        if cookies:
            driver.get('https://x.com')
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.get('https://x.com/i/grok')
            
            # Check if cookies are still valid
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="User-Name"]'))
                )
                user_name = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Name"]').text
                logging.info(f"Logged in with existing cookies as: {user_name}")
                return user_name
            except:
                logging.info("Existing cookies are invalid, fetching new ones")
        
        # If no valid cookies, fetch new ones from CookieCloud
        cookies = get_cookies_from_cloud()
        if not cookies:
            raise ValueError("No cookies received from CookieCloud")
        
        # Save new cookies
        save_cookies(cookies)
        
        # Use new cookies
        driver.get('https://x.com')
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get('https://x.com/i/grok')
        
        # Verify login
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
        if driver is not None:
            driver.quit()

if __name__ == '__main__':
    try:
        user_name = login_to_grok()
        print(f"Logged in as: {user_name}")
    except Exception as e:
        print(f"Login failed: {str(e)}")