import requests

def check_breaches(domain, api_key):
    headers = {
        'User-Agent': 'YourAppName',
        'hibp-api-key': api_key
    }
    url = f"https://haveibeenpwned.com/api/v3/breaches?domain={domain}"

    response = requests.get(url, headers=headers)
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
    domain = input("Enter the domain to check for breaches: ")
    api_key = "enter_here"
    check_breaches(domain, api_key)
