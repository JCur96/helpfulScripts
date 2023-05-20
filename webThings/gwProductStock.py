import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# url of the product you want to monitor
url = 'https://www.games-workshop.com/en-GB/Product-Example'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

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
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the product status on the webpage
    # 'product-status' should be replaced with the actual HTML id or class of the product status on the webpage
    product_status = soup.find('div', {'id': 'product-status'}).get_text().strip()

    if 'available' in product_status.lower():
        print('Product is available!')
        send_email()
    else:
        print('Product is not available yet.')

while True:
    check_availability()
    time.sleep(3600)  # Check every hour
###