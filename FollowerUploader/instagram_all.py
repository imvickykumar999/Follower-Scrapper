from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from scrapping import *  # Assuming scrapping contains utility functions like convert_to_numeric
import requests, os, json, time

script_dir = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(script_dir, 'sel_user')  # This will be inside the same folder

# Function to log in to Instagram
def user_login(driver):
    URL = 'https://www.instagram.com/'
    driver.get(URL)
    username = "bol7test"
    password = "Priyanka@123"

    try:
        time.sleep(5)
        login_button = driver.find_element(By.XPATH, "//button[.//div[text()='Log in']]")
        print('Login button:', login_button)
        
        # Find username and password fields and enter credentials
        items = driver.find_elements(By.CSS_SELECTOR, '._aa4b._add6._ac4d._ap35')
        items[0].send_keys(username)
        items[1].send_keys(password)
        
        time.sleep(5)
        login_button.click()
        time.sleep(5)
    except Exception as e:
        print(f"Login failed: {e}")


# Function to fetch influencer data from the API
def get_influencer_data():
    get_url = 'https://scrappedserver.pythonanywhere.com/get_influencer_profile_links/?platform=Instagram'
    headers = {
        'authorization': 'cbvcasdghcvsdhcvjhsdgjhasdjhsdadjasjdjkhasjhdgjasd'
    }

    try:
        response = requests.get(get_url, headers=headers)
        influencer_data = response.json()
        print(f"Total influencers: {len(influencer_data)}")

        if influencer_data is None:
            print('No influencer data available.')
            return
    except Exception as e:
        print(f"Error fetching influencer data: {e}")
        return

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ), options=options
    )

    # Perform Instagram login
    user_login(driver)

    try:
        # Allow Instagram to load fully before interacting
        time.sleep(5)

        # Dismiss notifications if they appear
        try:
            noti_item = driver.find_elements(By.CSS_SELECTOR, '.a9--._ap36._a9_0')
            if noti_item:
                noti_item[0].click()
            time.sleep(5)
        except Exception as e:
            print(f"Error dismissing notifications: {e}")

        # Process each influencer's profile
        user_no = 0
        for item in influencer_data[88:]:
            user_no += 1
            print(f'User ID: {item[0]}, User No: {user_no}, URL: {item[2]}')

            try:
                driver.get(item[2])  # Navigate to influencer page
                print('Navigated to influencer page.')
                time.sleep(5)

                try:
                    # Locate the follower count element
                    follower_count_elem = driver.find_element(By.XPATH, "//a[contains(@href, '/followers/')]/span/span")
                    text = follower_count_elem.get_attribute("title") or follower_count_elem.text
                    
                    if text:
                        print('Followers:', text)
                        if ',' in text:
                            text = text.replace(',', '')
                        subs = convert_to_numeric(text)
                        print(f"Subscriber count: {subs}")

                        # Get the influencer's username
                        h2_element = driver.find_element(By.XPATH, "//h2[contains(@class, 'x1lliihq')]")
                        username_text = h2_element.text

                        # Prepare influencer data for posting
                        influ_data = [item[0], 'Instagram', subs, username_text]
                        post_influencer_subscriber(influ_data)
                    else:
                        print("Follower count element found but it's empty.")

                except Exception as e:
                    print(f"Error extracting subscriber data: {e}")
                    print("HTML Source for Debugging:")
                    print(driver.page_source)  # Print page source for debugging

            except Exception as e:
                print(f"Error loading influencer page: {e}")
                continue

    finally:
        driver.close()  # Close the browser after processing all influencers


# Function to post the influencer subscriber data to the API
def post_influencer_subscriber(influ_data):
    post_url = 'https://scrappedserver.pythonanywhere.com/myendpoint'  # Update URL to localhost

    headers = {
        'authorization': 'cbvcasdghcvsdhcvjhsdgjhasdjhsdadjasjdjkhasjhdgjasd',
        'Content-Type': 'application/json',
    }

    payload = {
        'userid': influ_data[0],
        'platformname': influ_data[1],
        'followers': influ_data[2],
        'platformcredential': influ_data[3]
    }

    try:
        response = requests.post(post_url, data=json.dumps(payload, indent=4), headers=headers)
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error posting influencer data: {e}")

# Run the data collection process
get_influencer_data()

