import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from scrapping import convert_to_numeric  # Assuming convert_to_numeric is in scrapping module


def get_influencer_data():
    """Fetch influencer profile links and scrape data for each influencer."""
    get_url = 'https://scrappedserver.pythonanywhere.com/get_influencer_profile_links/?platform=Facebook'
    
    # Authorization headers
    headers = {
        'authorization': 'cbvcasdghcvsdhcvjhsdgjhasdjhsdadjasjdjkhasjhdgjasd'
    }

    try:
        # Fetch the influencer data from API
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        influencer_data = response.json()

        print(f"Total influencers fetched: {len(influencer_data)}")
    except requests.RequestException as e:
        print(f"Error fetching influencer data: {e}")
        return

    if not influencer_data:
        print('No influencer data found.')
        return

    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Login to Facebook
    login_to_facebook(driver)

    user_no = 0
    for item in influencer_data:
        print('\n\n\n')
        user_no += 1
        user_url = item[2]
        
        print(f"Getting data for {user_no} out of {len(influencer_data)} users.")
        print(f"User ID: {item[0]}")
        
        if user_url:
            scrape_facebook_data(driver, item, user_no)
        else:
            print("No URL found for this influencer.")
    
    # Close the WebDriver after all operations
    driver.quit()


def login_to_facebook(driver):
    """Logs into Facebook using Selenium WebDriver."""
    facebook_url = 'https://www.facebook.com/'
    email = "bol7test@gmail.com"
    password = "Rblogin227%"

    try:
        driver.get(facebook_url)
        time.sleep(5)
        
        # Find email, password fields and login button
        email_elem = driver.find_element(By.ID, "email")
        password_elem = driver.find_element(By.ID, "pass")
        login_button = driver.find_element(By.NAME, "login")

        # Enter login credentials
        email_elem.send_keys(email)
        password_elem.send_keys(password)
        time.sleep(2)

        # Click the login button
        login_button.click()
        time.sleep(20)
        print("Logged into Facebook successfully.")
    except Exception as e:
        print(f"Error logging into Facebook: {e}")
        driver.quit()


def scrape_facebook_data(driver, item, user_no):
    """Scrapes the username and followers count from the Facebook page."""
    try:
        driver.get(item[2])  # Navigate to the user's Facebook profile
        time.sleep(5)

        # Check if the content is unavailable (account deleted or private)
        try:
            unavailable_message = driver.find_element(By.XPATH, "//*[contains(text(), 'This content isn\'t available')]")
            print(f"User {user_no}: Profile is unavailable, skipping.")
            return  # Skip this profile
        except:
            pass  # Continue scraping if the profile is available

        # Extract username, or set to 'Unknown' if not found
        username = "Unknown"
        try:
            username_elem = driver.find_element(By.CSS_SELECTOR, "div > span > h1.x1heor9g")
            username = username_elem.text
            print(f"Username: {username}")
        except Exception as e:
            print(f"Error fetching username for user {user_no}: {e}")

        # Extract followers count, or set to 0 if not found
        followers_count = 0
        try:
            followers_link = driver.find_element(By.CSS_SELECTOR, "a[href*='followers']")
            followers_text = followers_link.text
            print(f"Followers text: {followers_text}")
            followers_count = convert_to_numeric(followers_text.split(' ')[0])
            print(f"Followers: {followers_count}")
        except Exception as e:
            print(f"Error fetching followers for user {user_no}: {e}")

        # Prepare data for submission
        influ_data = [item[0], 'Facebook', followers_count, username]
        post_influencer_subscriber(influ_data)

    except Exception as e:
        print(f"Error scraping data for user {user_no}: {e}")

def convert_to_numeric(value):
    """Converts a string with K/M suffix to a numeric value."""
    value = value.lower()
    if 'k' in value:
        return int(float(value.replace('k', '')) * 1000)
    elif 'm' in value:
        return int(float(value.replace('m', '')) * 1000000)
    return int(value)

def post_influencer_subscriber(influ_data):
    """Posts influencer data to the server."""
    post_url = 'https://scrappedserver.pythonanywhere.com/myendpoint'
    
    headers = {
        'authorization': 'cbvcasdghcvsdhcvjhsdgjhasdjhsdadjasjdjkhasjhdgjasd',
        'Content-Type': 'application/json'
    }

    payload = {
        'userid': influ_data[0],
        'platformname': influ_data[1],
        'followers': influ_data[2],
        'platformcredential': influ_data[3]
    }

    try:
        response = requests.post(post_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print(f"Data posted successfully: {response.text}")
    except requests.RequestException as e:
        print(f"Error posting data: {e}")

if __name__ == "__main__":
    get_influencer_data()
