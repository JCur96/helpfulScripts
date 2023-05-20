from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# options=Options()
# firefox_profile = FirefoxProfile()
# firefox_profile.set_preference("javascript.enabled", False)
# options.profile = firefox_profile

# url of the product you want to monitor
url = 'https://www.games-workshop.com/en-GB/astra-militarum-cadian-heavy-weapons-squad-2023'

def send_email():
    from_addr = "your_email@example.com"
    to_addr = "recipient_email@example.com"
    password = "yourpassword"

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "Product Availability Alert"

    body = "The product is now available at: " + url
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()

def check_availability():
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    # driver.get('https://www.mozilla.org/en-GB/firefox/new/')
    # driver = webdriver.Firefox(executable_path='/drivers/geckodriver.exe')
    driver.get(url)
    # driver.get('https://google.com')

    # Locate the product status on the webpage
    # 'product-details__stock-message' should be replaced with the actual HTML id or class of the product status on the webpage
    # product_status_element = driver.find_element_by_class_name('product-details__stock-message')
    # product_status_element = driver.find_element_by_css_selector('.product-details__stock-message')
    wait = WebDriverWait(driver, 10)  # wait up to 10 seconds
    # product_status_element = driver.find_element('css selector', 'span.product-details__stock-message')
    product_status_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.product-details__stock-message.product-details__stock-message--inStock.test-availability-inStock')))

    print(product_status_element.text.strip())

    if product_status_element is None:
        print('Could not find product status on the page.')
        return

    product_status = product_status_element.text.strip()

    if 'in stock' in product_status.lower():
        print('Product is available!')
        # send_email()
    else:
        print('Product is not available yet.')

    driver.quit()

while True:
    check_availability()
    time.sleep(3600)  # Check every hour

# import requests
# from bs4 import BeautifulSoup
# import time
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# # url of the product you want to monitor
# url = 'https://www.games-workshop.com/en-GB/astra-militarum-cadian-heavy-weapons-squad-2023'

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

# def send_email():
#     from_addr = "your_email@example.com"
#     to_addr = "recipient_email@example.com"
#     password = "yourpassword"

#     msg = MIMEMultipart()
#     msg['From'] = from_addr
#     msg['To'] = to_addr
#     msg['Subject'] = "Product Availability Alert"

#     body = "The product is now available at: " + url
#     msg.attach(MIMEText(body, 'plain'))

#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login(from_addr, password)
#     text = msg.as_string()
#     server.sendmail(from_addr, to_addr, text)
#     server.quit()

# def check_availability():
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Locate the product status on the webpage
#     # 'product-status' should be replaced with the actual HTML id or class of the product status on the webpage
#     product_status = soup.find('span', {'class': 'product-details__stock-message product-details__stock-message--inStock test-availability-inStock'}).get_text().strip()

#     if 'in stock' in product_status.lower():
#         print('Product is available!')
#         # send_email()
#     else:
#         print('Product is not available yet.')

# # while True:
#     check_availability()
#     time.sleep(3600)  # Check every hour
###