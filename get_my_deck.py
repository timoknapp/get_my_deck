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
sent_notifications_for_devices = set()

def log(message):
    print(f"{datetime.now()}: {message}")

def start():
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=browser_options)
    driver.get(url)
    return driver

def refresh(driver):
    driver.get(url)

def quit(driver):
    driver.quit()

def send_email(deckname, deckprice, email, password, send_to_email, smtp_host):
    log(f"Sending email for {deckname}")
    subject = "Steam Deck In Stock"
    message = f"{deckname} in Stock for {deckprice} https://store.steampowered.com/sale/steamdeckrefurbished"
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

def check_deck_status(decktitle, deckstatus, deckprice, email, password, send_to_email, smtp_host, devices_to_monitor):
    decktitle = decktitle.strip()
    deckname = decktitle.split(" - ")[0]
    if devices_to_monitor and devices_to_monitor != [''] and deckname not in devices_to_monitor:
        log(f"{deckname} - Not in the list of devices to monitor")
        return 0
    if "add" in deckstatus.lower():
        if deckname not in sent_notifications_for_devices:
            log(f"{deckname} - In Stock for {deckprice}")
            send_email(deckname, deckprice, email, password, send_to_email, smtp_host)
            sent_notifications_for_devices.add(deckname)
        else:
            log(f"{deckname} - Still in Stock for {deckprice}, not sending another email")
        status = 1
    else:
        log(f"{deckname} - Out of Stock")
        if deckname in sent_notifications_for_devices:
            log(f"{deckname} - Out of Stock again, will send email if it comes back in stock")
            sent_notifications_for_devices.remove(deckname)
        status = 0
    return status

def runner(driver, email, password, send_to_email, smtp_host, devices_to_monitor):
    all_btn = driver.find_elements(By.XPATH, "//*[@id='SaleSection_33131']")
    if not all_btn:
        log("No elements found with the given XPath.")
        return 0, 0
    x = all_btn[0].text
    decks = x.split("\n")
    for i in range(0, len(decks), 3):
        decktitle = decks[i]
        deckstatus = decks[i+1]
        deckprice = decks[i+2]
        if "512 GB OLED" in decktitle:
            check_deck_status(decktitle, deckstatus, deckprice, email, password, send_to_email, smtp_host, devices_to_monitor)
        elif "1TB OLED" in decktitle:
            check_deck_status(decktitle, deckstatus, deckprice, email, password, send_to_email, smtp_host, devices_to_monitor)
        elif "64 GB LCD" in decktitle:
            check_deck_status(decktitle, deckstatus, deckprice, email, password, send_to_email, smtp_host, devices_to_monitor)
        elif "256 GB LCD" in decktitle:
            check_deck_status(decktitle, deckstatus, deckprice, email, password, send_to_email, smtp_host, devices_to_monitor)
        elif "512 GB LCD" in decktitle:
            check_deck_status(decktitle, deckstatus, deckprice, email, password, send_to_email, smtp_host, devices_to_monitor)
    return

def get_my_deck(email, password, send_to_email, smtp_host, test_email, refresh_time, devices_to_monitor):
    if test_email:
        send_email("Test Deck", "0", email, password, send_to_email, smtp_host)
        log("Test email sent. Exiting...")
        return

    start_time = 10
    driver = start()
    time.sleep(start_time)  # Wait for the page to load
    log("Started Scraper")
    while True:
        try:
            runner(driver, email, password, send_to_email, smtp_host, devices_to_monitor)
            refresh(driver)
            log(f"Reloading page in {refresh_time} seconds...")
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
    parser.add_argument('--devices_to_monitor', nargs='+', help='List of devices to monitor, separated by space. e.g. "Steam Deck 512 GB OLED" "Steam Deck 1TB OLED"')
    args = parser.parse_args()

    # Check for arguments or environment variables
    email = args.email or os.getenv('EMAIL')
    password = args.password or os.getenv('PASSWORD')
    send_to_email = args.send_to_email or os.getenv('SEND_TO_EMAIL')
    smtp_host = args.smtp_host or os.getenv('SMTP_HOST')
    test_email = args.test_email or os.getenv('TEST_EMAIL', 'false').lower() == 'true'
    refresh_time = args.refresh_time or int(os.getenv('REFRESH_TIME', 3600))
    devices_to_monitor = args.devices_to_monitor or os.getenv('DEVICES_TO_MONITOR', '').split(',')

    if not email or not password or not send_to_email or not smtp_host:
        parser.error('Email, password, send_to_email, and smtp_host must be provided either as arguments or environment variables.')

    get_my_deck(email, password, send_to_email, smtp_host, test_email, refresh_time, devices_to_monitor)
