import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from scrapping import convert_to_numeric


def login_user(driver, username, password):
    """
    Logs the user into Twitter.
    """
    try:
        time.sleep(10)
        username_field = driver.find_element(By.NAME, "text")
        username_field.send_keys(username)

        next_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
        next_button.click()

        time.sleep(10)
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)

        login_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Log in')]")
        login_button.click()

        time.sleep(5)
        print("Logged in successfully.")
    except Exception as e:
        print(f"Error during login: {e}")


def fetch_influencer_data():
    """
    Fetches influencer data from the API and processes each influencer profile.
    """
    api_url = 'https://www.influencerhiring.com/get_influencer_profile_links/?platform=Twitter'
    headers = {'authorization': 'cbvcasdghcvsdhcvjhsdgjhasdjhsdadjasjdjkhasjhdgjasd'}
    user_data_dir = '~/Documents/sel_user'

    try:
        response = requests.get(api_url, headers=headers)
        influencer_data = response.json()
        print(f"Total influencers fetched: {len(influencer_data)}")
    except Exception as e:
        print(f"Error fetching influencer data: {e}")
        return

    if not influencer_data:
        print("No influencer data available.")
        return

    # Set up Chrome driver with user data
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    process_influencers(driver, influencer_data)

    driver.quit()


def process_influencers(driver, influencer_data):
    """
    Processes each influencer by navigating to their profile and extracting data.
    """
    username = "7840002988"
    password = "Manu@123"

    for idx, item in enumerate(influencer_data):
        print('\n\n\n')
        user_id, platform, profile_url = item[:3]
        print(f"Processing user {idx + 1}/{len(influencer_data)}: {user_id}")

        try:
            driver.get(profile_url)
            time.sleep(5)

            # Check if login is required
            if 'login' in driver.current_url:
                print("Logging in to Twitter...")
                login_user(driver, username, password)
                time.sleep(30)

            extract_influencer_data(driver, item)
        except Exception as e:
            print(f"Error processing user {user_id}: {e}")
            continue


def extract_influencer_data(driver, item):
    """
    Extracts the necessary influencer data from the profile page.
    """
    try:
        username_element = driver.find_element(By.CSS_SELECTOR, '[class*="css-146c3p1"]')
        username_text = username_element.text

        followers_element = driver.find_element(By.XPATH, "//a[contains(@href, 'verified_followers')]")
        followers_count = convert_to_numeric(followers_element.text.split(' ')[0])

        influencer_data = [item[0], 'Twitter', followers_count, username_text]
        print(f"Extracted data: {influencer_data}")

        post_influencer_subscriber(influencer_data)
    except Exception as e:
        print(f"Error extracting data for {item[0]}: {e}")


def post_influencer_subscriber(influ_data):
    """
    Posts the influencer data to the server.
    """
    post_url = 'https://www.influencerhiring.com/post_influencer_profiledata/'
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
        print(f"Post response: {response.text}")
    except Exception as e:
        print(f"Error posting influencer data: {e}")


if __name__ == "__main__":
    fetch_influencer_data()
