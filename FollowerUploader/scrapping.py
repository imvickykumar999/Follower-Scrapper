import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import numerize
from bs4 import BeautifulSoup    

def convert_to_numeric(value_str):
    multipliers = {
        'K': 1e3,
        'M': 1e6,
        'B': 1e9,
        'T': 1e12
    }
    
    if value_str[-1] in multipliers:
        return int(float(value_str[:-1]) * multipliers[value_str[-1]])
    if ',' in value_str:
        return value_str.replace(',', '')
    else:
        return int(value_str)

def youtube_scraping(user_data):
    try:
        options = webdriver.ChromeOptions()
        
        # options.add_argument("--headless")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        URL = user_data
        print(URL)
        driver.get(URL)
        
        time.sleep(5)
        
        subscriber_count_element = driver.find_element(By.CSS_SELECTOR, "#subscriber-count")
        print(subscriber_count_element.text.split(' ')[0])
        
        total_sub = convert_to_numeric(subscriber_count_element.text.split(' ')[0])
        print(total_sub)
        driver.close()
        return total_sub
    except:
        return 0



def instagram_scrapping(link):
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("start-maximized")
        # options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        URL = link
        driver.get(URL)
        username="bol7test"
        password="Manu@123"
        time.sleep(5)

        # count = driver.find_elements(By.CLASS_NAME, '_ac2a')

        # print(count[1].text)
        print('getting here')
        subscriber_count_element = driver.find_elements(By.CLASS_NAME, '_ac2a')

        if len(subscriber_count_element) > 1:
            subscriber_count_element = subscriber_count_element[1]
            text = subscriber_count_element.text
            if ',' in text:
                text = text.replace(',','')
            subs = convert_to_numeric(text)
            driver.close()
            print(subs)
            return subs
        else:
            print("Not enough elements found with the given class name.")
            
    except:
        driver.close()
        return 0


def facebook_scrapping(link):
    try:
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)   
        URL =link
        driver.get(URL)
        time.sleep(5)
        name = URL.split('/')[-2]
        print(name)
        subscriber_count_element = driver.find_elements(By.CSS_SELECTOR, f'a[href="https://www.facebook.com/{name}/followers/"]')
        subs = convert_to_numeric(subscriber_count_element[0].text.split(' ')[0])
        driver.close()
        return subs
    except:
        driver.close()
        return 0

def linkedin_scrapping(link):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)   
        URL ='https://www.linkedin.com/login/'
        driver.get(URL)
        # page_source = driver.page_source
        # # print(page_source)
        username = 'info@influencerhiring.com'
        password = 'hiring+info@1'
        # Find element by CSS selector
        time.sleep(5)

        email_elem = driver.find_element(By.ID, "username")
        password_elem = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CLASS_NAME, "btn__primary--large")

        email_elem.send_keys(username)
        password_elem.send_keys(password)
        login_button.click()
        time.sleep(5)

        user_url = link
        driver.get(user_url)

        time.sleep(5)

        subscriber_count_element = driver.find_elements(By.CLASS_NAME, "ph5")

        # If you want to print the text inside that element:
        details = subscriber_count_element[0].text.split('\n')
        print(details)
        items_with_followers = [item for item in details if 'followers' in item]
        
        driver.close()
        return int(items_with_followers[0].split(' ')[0].replace(',',''))
    
    except:
        driver.close()
        return 0

def twitter_scrapping(link):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)   
        URL =link
        driver.get(URL)
        time.sleep(5)
        subscriber_count_element = driver.find_elements(By.CSS_SELECTOR, ".css-1dbjc4n.r-13awgt0.r-18u37iz.r-1w6e6rj > div")
        subs = convert_to_numeric(subscriber_count_element[1].text.split(' ')[0])
        driver.close()
        print(subs)
        return subs
    except:
        driver.close()
        return 0

def twitch_scrapping(link):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)   
        URL =link
        driver.get(URL)
        time.sleep(5)
        subscriber_count_element = driver.find_element(By.XPATH, "//p[contains(text(), 'followers')]")
        subs = convert_to_numeric(subscriber_count_element.text.split(' ')[0])
        driver.close()
        return subs
    except:
        driver.close()
        return 0
