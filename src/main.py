import requests
import time
import hashlib
import threading
import json

def fetch_website_content(url):
    response = requests.get(url)
    return response.text

def compute_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def send_slack_notification(message, webhook_url):
    data = {"text": message}
    response = requests.post(webhook_url, json=data)
    if response.status_code != 200:
        print(f"Slack notification failed. Status code: {response.status_code}")

def monitor_website(url, webhook_url, interval=60):
    print(f"Monitoring website: {url}")
    last_hash = None
    while True:
        try:
            current_content = fetch_website_content(url)
            current_hash = compute_hash(current_content)
            if last_hash is not None and current_hash != last_hash:
                send_slack_notification(f":bulb: Website content has changed! URL: {url}", webhook_url)
            last_hash = current_hash
        except Exception as e:
            send_slack_notification(f":warning: Error fetching website data: {e} URL: {url}", webhook_url)
        time.sleep(interval)


def start_monitoring(urls, webhook_url, interval=60):
    threads = []
    for url in urls:
        thread = threading.Thread(target=monitor_website, args=(url, webhook_url, interval))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
        
# Read configuration from config.json file
with open('config.json') as config_file:
    config = json.load(config_file)

# Incoming Webhook URL for Slack
webhook_url = config['SLACK_WEBHOOK_URL']

# List of URLs of websites to be monitored
urls_to_monitor = [
    'https://example.com',
    'https://example.org'
]

start_monitoring(urls_to_monitor, webhook_url)