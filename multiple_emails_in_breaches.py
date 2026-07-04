import re
import sys
import time

from email_breaches import check_email
from hibp import get_api_key, get_setting

if __name__ == "__main__":
    if len(sys.argv) > 1:
        emails = sys.argv[1:]
    else:
        emails = re.split(r"[\s,]+", get_setting("HIBP_EMAILS") or "")

    emails = list(dict.fromkeys(e for e in emails if e))
    if not emails:
        print("Usage: python multiple_emails_in_breaches.py <email1> <email2> ... (or set HIBP_EMAILS in .env)")
        raise SystemExit(1)

    api_key = get_api_key()
    if not api_key:
        print("Error: set the HIBP_API_KEY environment variable.", file=sys.stderr)
        raise SystemExit(2)

    for i, email in enumerate(emails):
        if i:
            time.sleep(1.5)
        check_email(email, api_key)
