import requests
import hashlib

def hash_password(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    return sha1password

def check_password(password):
    sha1password = hash_password(password)
    prefix, suffix = sha1password[:5], sha1password[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching data from HIBP API.")
        return

    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            print(f"Password has been breached! It has appeared in {count} breaches.")
            return

    print("Your password has not appeared in any breach.")

if __name__ == "__main__":
    password = input("Enter the password to check: ")
    check_password(password)
