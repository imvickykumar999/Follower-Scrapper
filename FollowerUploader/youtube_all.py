from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import requests
import json

def convert_to_numeric(subscriber_text):
    # Helper function to convert subscriber count to a numeric value
    if 'K' in subscriber_text:
        return int(float(subscriber_text.replace('K', '').replace(',', '').strip()) * 1000)
    elif 'M' in subscriber_text:
        return int(float(subscriber_text.replace('M', '').replace(',', '').strip()) * 1000000)
    elif 'B' in subscriber_text:
        return int(float(subscriber_text.replace('B', '').replace(',', '').strip()) * 1000000000)
    else:
        try:
            return int(subscriber_text.replace(',', '').strip())
        except ValueError:
            return 0

def get_influencer_data():
    get_url = 'https://scrappedserver.pythonanywhere.com/get_influencer_profile_links/?platform=Youtube'
    
    headers = {
        'authorization': 'cbvcasdghcvsdhcvjhsdgjhasdjhsdadjasjdjkhasjhdgjasd'
    }
    
    data = requests.get(get_url, headers=headers)
    influencer_data = json.loads(data.text)
    print(len(influencer_data))
    
    if not influencer_data:
        print('data does not exist!!')
    else:
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        user_no = 0
        for item in influencer_data:
            user_no += 1
            print(f'user id => {item[0]}')
            print(f'user no.==< {user_no} > out of {len(influencer_data)} in progress')
            URL = item[2].split("?")[0] if item[2] != 'NA' else None  # Remove query parameters if any
            
            if URL:  # Check if URL is valid
                print(item, URL)
                try:
                    driver.get(URL)
                    time.sleep(3)  # Allow some time for the page to load
                except Exception as e:
                    print(f"Error opening URL {URL}: {str(e)}")
                    continue

                try:
                    # Locate the element that contains the channel name
                    channel_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "yt-content-metadata-view-model .yt-core-attributed-string"))
                    )
                    channel_name = channel_element.text
                    print(f"Channel Name: {channel_name}")

                    # Locate the element that contains the subscriber count
                    subscriber_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'subscribers')]"))
                    )
                    subscriber_count_text = subscriber_element.text.split(' ')[0]

                    subs = convert_to_numeric(subscriber_count_text)
                    print(f"Subscribers: {subs}")

                    influ_data = [item[0], 'Youtube', subs, channel_name]
                    post_influencer_subscriber(influ_data)

                except TimeoutException:
                    print(f"Timeout while trying to locate elements on page: {URL}")
                except Exception as e:
                    print(f"Error occurred: {str(e)}")
            else:
                print(f"Invalid URL for user id {item[0]}: {item[2]}")

        driver.quit()

        
def post_influencer_subscriber(influ_data):
    post_url = 'https://scrappedserver.pythonanywhere.com/myendpoint'

    headers = {
        'authorization': 'cbvcasdghcvsdhcvjhsdgjhasdjhsdadjasjdjkhasjhdgjasd',
        'Content-Type': 'application/json'  # Make sure the content type is set to application/json
    }
    
    payload = {
        'userid': influ_data[0],
        'platformname': influ_data[1],
        'followers': influ_data[2],
        'platformcredential': influ_data[3]
    }

    data = requests.post(post_url, data=json.dumps(payload, indent=4), headers=headers)
    print(data.text)

get_influencer_data()
