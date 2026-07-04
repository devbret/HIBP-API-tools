import hashlib
from getpass import getpass

import requests

def hash_password(password):
    return hashlib.sha1(password.encode("utf-8"), usedforsecurity=False).hexdigest().upper()

def check_password(password):
    sha1password = hash_password(password)
    prefix, suffix = sha1password[:5], sha1password[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url, headers={"Add-Padding": "true"}, timeout=20)

    if response.status_code != 200:
        print(f"Error fetching data from HIBP API (HTTP {response.status_code}).")
        return

    for line in response.text.splitlines():
        h, _, count = line.partition(":")
        if h == suffix and int(count) > 0:
            print(f"Password has been breached! It has appeared in {count} breaches.")
            return

    print("Your password has not appeared in any breach.")

if __name__ == "__main__":
    password = getpass("Enter the password to check: ")
    check_password(password)
