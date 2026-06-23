import os

import requests
from dotenv import load_dotenv
from getpass import getpass
from urllib.parse import quote

def check_email(email, api_key):
    headers = {
        'User-Agent': 'EmailBreachCheckTool',
        'hibp-api-key': api_key,
    }
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{quote(email, safe='')}?truncateResponse=false"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        breaches = response.json()
        print(f"Breaches found for {email}:")
        for breach in breaches:
            print(f"- {breach['Name']}: {breach['Description']}")
    elif response.status_code == 404:
        print(f"No breaches found for {email}.")
    else:
        print("Error occurred while fetching breach information.")

if __name__ == "__main__":
    load_dotenv()
    email = input("Enter your email address to check for breaches: ")
    api_key = os.getenv("HIBP_API_KEY") or getpass("Enter your HIBP API key here: ")
    check_email(email, api_key)
