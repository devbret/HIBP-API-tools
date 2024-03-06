import requests

def check_email_in_pastes(email, api_key):
    headers = {
        'User-Agent': 'PasteCheckTool',
        'hibp-api-key': api_key,
    }
    url = f"https://haveibeenpwned.com/api/v3/pasteaccount/{email}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pastes = response.json()
        if pastes:
            print(f"Email {email} has appeared in the following pastes:")
            for paste in pastes:
                print(f"- Source: {paste['Source']} | ID: {paste['Id']} | Title: {paste.get('Title', 'N/A')} | Date: {paste['Date']}")
        else:
            print(f"No pastes found for {email}.")
    elif response.status_code == 404:
        print(f"No pastes found for {email}.")
    else:
        print("Error occurred while fetching paste information.")

if __name__ == "__main__":
    email = input("Enter your email address to check for pastes: ")
    api_key = "enter_here"
    check_email_in_pastes(email, api_key)
