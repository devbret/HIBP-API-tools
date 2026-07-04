import sys
from urllib.parse import quote

from hibp import error_message, hibp_get, strip_html

def format_breach(breach):
    return [
        ("Name", breach.get("Name")),
        ("Title", breach.get("Title")),
        ("Domain", breach.get("Domain")),
        ("Breach date", breach.get("BreachDate")),
        ("PwnCount", breach.get("PwnCount")),
        ("Description", strip_html(breach.get("Description"))),
        ("Data classes compromised", ", ".join(breach.get("DataClasses") or [])),
        ("Is verified", breach.get("IsVerified")),
        ("Is fabricated", breach.get("IsFabricated")),
        ("Is sensitive", breach.get("IsSensitive")),
        ("Is retired", breach.get("IsRetired")),
        ("Is spam list", breach.get("IsSpamList")),
    ]

def get_breach_details(breach_name):
    resp = hibp_get(f"/breach/{quote(breach_name, safe='')}", user_agent="BreachDetailsTool")
    if resp.status_code == 200:
        breach = resp.json()
        print(f"Details for {breach_name}:")
        for label, value in format_breach(breach):
            print(f"- {label}: {value}")
    elif resp.status_code == 404:
        print(f"No breach found with the name {breach_name}.")
    else:
        print(f"Error occurred while fetching breach details ({error_message(resp)}).", file=sys.stderr)

if __name__ == "__main__":
    breach_name = input("Enter the name of the breach to get details: ")
    get_breach_details(breach_name)
