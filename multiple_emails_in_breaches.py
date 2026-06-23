import requests
import sys
import time
import os
from urllib.parse import quote

from dotenv import load_dotenv

def check_email(email, api_key):
    headers = {
        'User-Agent': 'EmailBreachCheckTool',
        'hibp-api-key': api_key,
    }
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{quote(email, safe='')}?truncateResponse=false"

    wait_time = 1.5 
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            breaches = response.json()
            print(f"Breaches found for {email}:")
            for breach in breaches:
                print(f"- {breach['Name']}: {breach['Description']}")
            break
        elif response.status_code == 404:
            print(f"No breaches found for {email}.")
            break
        elif response.status_code == 429:
            print("Rate limit exceeded, waiting to retry...")
            time.sleep(wait_time)
            wait_time *= 2
        else:
            print(f"Error occurred while fetching breach information for {email}. Response Code: {response.status_code}")
            break

if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) <= 1:
        print("Usage: HIBP_API_KEY=... python multiple_emails_in_breaches.py <email1> <email2> ...")
        raise SystemExit(1)

    api_key = os.getenv("HIBP_API_KEY")
    if not api_key:
        print("Error: set the HIBP_API_KEY environment variable.", file=sys.stderr)
        raise SystemExit(2)

    emails = sys.argv[1:]
    for email in emails:
        check_email(email, api_key)
        time.sleep(1.5)
