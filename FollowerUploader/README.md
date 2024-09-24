# `.onion` **scrapping**

Using Selenium to interact with `.onion` URLs requires configuring it to use the Tor network. `.onion` URLs are part of the **Tor** network (The Onion Router), which provides anonymity for users. To access `.onion` URLs via Selenium, you need to run a **Tor browser** or a **Tor proxy** and configure Selenium's WebDriver to use it.

Here’s a step-by-step guide on how to use Selenium with `.onion` URLs:

### Prerequisites:
1. **Tor Browser**: Download and install the Tor Browser from the official website: [https://www.torproject.org/download/](https://www.torproject.org/download/).
2. **Selenium**: Install Selenium WebDriver using pip:
   ```bash
   pip install selenium
   ```
3. **Tor executable**: Ensure that the Tor executable is accessible on your machine.

### Method 1: Using Tor with Firefox and Selenium

#### Step-by-Step Configuration:

1. **Install GeckoDriver**:
   For Selenium to work with Firefox, you need GeckoDriver. You can install it via:
   - Download the appropriate version from [here](https://github.com/mozilla/geckodriver/releases).
   - Alternatively, install it via the **webdriver_manager** library:
     ```bash
     pip install webdriver-manager
     ```

2. **Run Tor in the Background**:
   Tor needs to be running in the background to route traffic through the network. If you installed the Tor Browser, it usually runs Tor automatically when you start the browser. You can also run Tor separately using the Tor executable.

3. **Configure Firefox to Use the Tor Network**:
   You will configure Firefox's proxy settings to connect to the Tor network (default SOCKS5 proxy on `127.0.0.1:9150` for the Tor Browser).

Here’s a Python script to set up Selenium with Tor:

```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

def configure_tor_with_selenium():
    # Set up Firefox options
    options = Options()
    
    # Make sure Tor is running locally (default SOCKS proxy address for Tor Browser)
    options.set_preference("network.proxy.type", 1)  # Set proxy type to manual
    options.set_preference("network.proxy.socks", "127.0.0.1")  # Tor's local SOCKS5 proxy address
    options.set_preference("network.proxy.socks_port", 9150)  # Tor Browser proxy port
    options.set_preference("network.proxy.socks_remote_dns", True)  # Route DNS through Tor
    options.set_preference("places.history.enabled", False)  # Disable browser history
    options.set_preference("privacy.clearOnShutdown.offlineApps", True)
    options.set_preference("privacy.clearOnShutdown.passwords", True)
    options.set_preference("privacy.clearOnShutdown.siteSettings", True)
    options.set_preference("privacy.sanitize.sanitizeOnShutdown", True)

    # Initialize the WebDriver with the options
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    
    return driver

if __name__ == "__main__":
    driver = configure_tor_with_selenium()
    
    # Visit an .onion URL (make sure the URL is correct)
    onion_url = "http://exampleonionurl.onion"
    driver.get(onion_url)
    
    # You can interact with the page as usual using Selenium commands
    print(driver.title)  # Print the title of the page to verify it's loaded
    
    driver.quit()
```

### Key Points:
- **SOCKS Proxy**: The Tor network uses a SOCKS5 proxy by default, which is configured in the script (`127.0.0.1:9150` for the Tor Browser).
- **FireFox Options**: Several privacy-related options are set to ensure no data is saved locally.
  
### Method 2: Using Tor and Chrome (with the Tor Expert Bundle)

1. **Download the Tor Expert Bundle**:
   - You can download the [Tor Expert Bundle](https://www.torproject.org/download/tor/) for your operating system, which allows you to run Tor independently of the Tor Browser.

2. **Configure Chrome to Use the Tor Network**:
   You can set up Chrome to use the Tor SOCKS5 proxy, similar to the Firefox configuration above, but Chrome does not natively support SOCKS5 DNS resolution, so you will also need to configure DNS resolution to route through Tor.

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def configure_tor_with_chrome():
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    
    # Set up the Tor SOCKS5 proxy
    options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
    
    # Initialize Chrome WebDriver with the options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    return driver

if __name__ == "__main__":
    driver = configure_tor_with_chrome()
    
    # Visit an .onion URL (make sure the URL is correct)
    onion_url = "http://exampleonionurl.onion"
    driver.get(onion_url)
    
    # You can interact with the page as usual using Selenium commands
    print(driver.title)  # Print the title of the page to verify it's loaded
    
    driver.quit()
```

### Considerations:
- **Speed**: Browsing `.onion` URLs through Tor is generally slower due to the nature of the Tor network.
- **Security**: Always ensure that Tor is properly configured, and be cautious when browsing `.onion` sites as they can sometimes host malicious content.
- **Tor Browser**: Running the full Tor Browser is the safest way to ensure proper anonymity and security, as it is configured to work with the Tor network.

### Conclusion:
This setup should allow you to use Selenium with `.onion` URLs via the Tor network. Ensure that Tor is running and properly configured before running your script, and use the appropriate proxy settings based on the browser (Firefox or Chrome) you are using.
