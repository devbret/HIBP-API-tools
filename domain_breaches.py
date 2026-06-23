import os

import requests
from dotenv import load_dotenv
from getpass import getpass

def check_breaches(domain, api_key):
    headers = {
        'User-Agent': 'DomainBreachTool',
        'hibp-api-key': api_key
    }
    url = "https://haveibeenpwned.com/api/v3/breaches"

    response = requests.get(url, headers=headers, params={'domain': domain})
    if response.status_code == 200:
        breaches = response.json()
        if breaches:
            print(f"Breaches found for {domain}:")
            for breach in breaches:
                print(f"- {breach['Name']}: {breach['Description']}")
        else:
            print(f"No breaches found for {domain}.")
    else:
        print("Error occurred while fetching breach information.")

if __name__ == "__main__":
    load_dotenv()
    domain = input("Enter the domain to check for breaches: ")
    api_key = os.getenv("HIBP_API_KEY") or getpass("Enter your HIBP API key here: ")
    check_breaches(domain, api_key)
