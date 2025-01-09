import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime
import os

browser_options = Options()
browser_options.add_argument("--headless")
url = "https://store.steampowered.com/sale/steamdeckrefurbished"

def log(message):
    print(str(datetime.now())+": "+str(message))

def start():
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=browser_options)
    driver.get(url)
    return driver

def refresh(driver):
    driver.get(url)

def quit(driver):
    driver.quit()

def send_email(deck, email, password, send_to_email, smtp_host):
    log("Sending Email reminder...")
    subject = "Steam Deck In Stock"
    message = str(deck)+" in Stock https://store.steampowered.com/sale/steamdeckrefurbished"
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP(smtp_host, 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()

def check_deck_status(deck, email, password, send_to_email, smtp_host):
    deck = deck[1:] if deck.startswith("\n") else deck
    deck = deck.replace("\n", " - ")
    deckname = deck.split(" - ")[0]
    if "add" in deck.lower():
        log(str(deckname)+" - "+"In Stock")
        send_email(deckname, email, password, send_to_email, smtp_host)
        status = 1
    else:
        log(str(deckname)+" - "+"Out of Stock")
        status = 0
    return status

def runner(driver, email, password, send_to_email, smtp_host):
    all_btn = driver.find_elements(By.XPATH, "//*[@id='SaleSection_33131']")
    if not all_btn:
        log("No elements found with the given XPath.")
        return 0, 0
    x = all_btn[0].text
    if "€" in x:
        parts = x.split("€")
        if len(parts) >= 2:
            sd512GBoled = parts[0]
            sd1TBoled = parts[1]
            status_512gb = check_deck_status(sd512GBoled, email, password, send_to_email, smtp_host)
            status_1tb = check_deck_status(sd1TBoled, email, password, send_to_email, smtp_host)
            return status_512gb, status_1tb
        else:
            log("Unexpected text format: "+str(x))
            return 0, 0
    else:
        log("Unexpected text format: "+str(x))
        return 0, 0

def get_my_deck(email, password, send_to_email, smtp_host, test_email, refresh_time):
    if test_email:
        send_email("Test Deck", email, password, send_to_email, smtp_host)
        log("Test email sent. Exiting...")
        return

    start_time = 10
    driver = start()
    time.sleep(start_time)  # Wait for the page to load
    log("Started Scraper")
    while True:
        try:
            sd512, sd1024 = runner(driver, email, password, send_to_email, smtp_host)
            if sd512 or sd1024:
                log("Deck is in stock! Exiting...")
                quit(driver)
                break
            refresh(driver)
            log("Reloading page in "+str(refresh_time)+" seconds...")
            time.sleep(refresh_time)  # Refresh the page once per minute
        except Exception as e:
            print(e)
            quit(driver)
            driver = start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Steam Deck Stock Checker')
    parser.add_argument('--email', help='Email address to send notifications from')
    parser.add_argument('--password', help='Password for the email account')
    parser.add_argument('--send_to_email', help='Email address to send notifications to')
    parser.add_argument('--smtp_host', help='SMTP host for sending email')
    parser.add_argument('--test_email', action='store_true', help='Send a test email and exit')
    parser.add_argument('--refresh_time', type=int, default=3600, help='Time in seconds between page refreshes')
    args = parser.parse_args()

    # Check for arguments or environment variables
    email = args.email or os.getenv('EMAIL')
    password = args.password or os.getenv('PASSWORD')
    send_to_email = args.send_to_email or os.getenv('SEND_TO_EMAIL')
    smtp_host = args.smtp_host or os.getenv('SMTP_HOST')
    test_email = args.test_email or os.getenv('TEST_EMAIL', 'false').lower() == 'true'
    refresh_time = args.refresh_time or int(os.getenv('REFRESH_TIME', 3600))

    if not email or not password or not send_to_email or not smtp_host:
        parser.error('Email, password, send_to_email, and smtp_host must be provided either as arguments or environment variables.')

    get_my_deck(email, password, send_to_email, smtp_host, test_email, refresh_time)
