import sys
from urllib.parse import quote

from hibp import error_message, get_api_key, get_input, hibp_get, strip_html

def check_email(email, api_key):
    resp = hibp_get(
        f"/breachedaccount/{quote(email, safe='')}",
        user_agent="EmailBreachCheckTool",
        api_key=api_key,
        params={"truncateResponse": "false"},
    )
    if resp.status_code == 200:
        breaches = resp.json()
        print(f"Breaches found for {email}:")
        for breach in breaches:
            print(f"- {breach['Name']}: {strip_html(breach['Description'])}")
    elif resp.status_code == 404:
        print(f"No breaches found for {email}.")
    else:
        print(f"Error occurred while fetching breach information ({error_message(resp)}).", file=sys.stderr)

if __name__ == "__main__":
    email = get_input("HIBP_EMAIL", "Enter your email address to check for breaches: ")
    api_key = get_api_key(prompt=True)
    check_email(email, api_key)
