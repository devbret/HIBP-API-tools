import requests

def get_breach_details(breach_name, api_key):
    headers = {
        'User-Agent': 'BreachDetailsTool',
        'hibp-api-key': api_key,
    }
    url = f"https://haveibeenpwned.com/api/v3/breach/{breach_name}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        breach = response.json()
        print(f"Details for {breach_name}:")
        print(f"- Name: {breach['Name']}")
        print(f"- Title: {breach['Title']}")
        print(f"- Domain: {breach['Domain']}")
        print(f"- Breach date: {breach['BreachDate']}")
        print(f"- PwnCount: {breach['PwnCount']}")
        print(f"- Description: {breach['Description']}")
        print(f"- Data classes compromised: {', '.join(breach['DataClasses'])}")
        print(f"- Is verified: {breach['IsVerified']}")
        print(f"- Is fabricated: {breach['IsFabricated']}")
        print(f"- Is sensitive: {breach['IsSensitive']}")
        print(f"- Is retired: {breach['IsRetired']}")
        print(f"- Is spam list: {breach['IsSpamList']}")
    elif response.status_code == 404:
        print(f"No breach found with the name {breach_name}.")
    else:
        print("Error occurred while fetching breach details.")

if __name__ == "__main__":
    breach_name = input("Enter the name of the breach to get details: ")
    api_key = "your_api_key_here"
    get_breach_details(breach_name, api_key)
