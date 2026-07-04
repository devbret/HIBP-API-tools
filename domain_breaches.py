import sys

from hibp import error_message, get_input, hibp_get, strip_html

def check_breaches(domain):
    resp = hibp_get("/breaches", user_agent="DomainBreachTool", params={"domain": domain})
    if resp.status_code == 200:
        breaches = resp.json()
        if breaches:
            print(f"Breaches found for {domain}:")
            for breach in breaches:
                print(f"- {breach['Name']}: {strip_html(breach['Description'])}")
        else:
            print(f"No breaches found for {domain}.")
    else:
        print(f"Error occurred while fetching breach information ({error_message(resp)}).", file=sys.stderr)

if __name__ == "__main__":
    domain = get_input("HIBP_DOMAIN", "Enter the domain to check for breaches: ")
    if not domain:
        print("Error: no domain provided.", file=sys.stderr)
        raise SystemExit(1)
    check_breaches(domain)
