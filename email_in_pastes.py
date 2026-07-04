import sys
from urllib.parse import quote

from hibp import error_message, get_api_key, get_input, hibp_get

def check_email_in_pastes(email, api_key):
    resp = hibp_get(
        f"/pasteaccount/{quote(email, safe='')}",
        user_agent="PasteCheckTool",
        api_key=api_key,
    )
    if resp.status_code == 200:
        pastes = resp.json()
        if pastes:
            print(f"Email {email} has appeared in the following pastes:")
            for paste in pastes:
                print(
                    f"- Source: {paste['Source']} | ID: {paste['Id']} | "
                    f"Title: {paste.get('Title') or 'N/A'} | Date: {paste.get('Date') or 'N/A'}"
                )
        else:
            print(f"No pastes found for {email}.")
    elif resp.status_code == 404:
        print(f"No pastes found for {email}.")
    else:
        print(f"Error occurred while fetching paste information ({error_message(resp)}).", file=sys.stderr)

if __name__ == "__main__":
    email = get_input("HIBP_EMAIL", "Enter your email address to check for pastes: ")
    api_key = get_api_key(prompt=True)
    check_email_in_pastes(email, api_key)
