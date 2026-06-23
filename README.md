# Have I Been Pwned API Tools

A comprehensive command-line toolkit for interacting with the Have I Been Pwned API, covering individual breach lookups, email breach checks, advanced stealer log queries and more.

## Application Overview

This repo bundles eight scripts each targeting a distinct HIBP endpoint. Most scripts require a personal HIBP API key and the project is designed to run in a standard Python virtual environment on Linux, with dependencies managed through a `requirements.txt` file.

The toolkit emphasizes reliability and automation. This makes it suitable not just for interactive checks but for repeatable workflows designed to identify exposed credentials and compromised assets across emails, domains and passwords.

Overall, the project serves as both a practical monitoring suite and a demonstration of secure, well-structured API integration across multiple HIBP services.

## Basic Setup Instructions

Below are instructions for installing and running this application on a Linux machine.

### Programs Needed

- [Git](https://git-scm.com/downloads)

- [Python](https://www.python.org/downloads/)

### Steps

1. Install the above programs

2. Open a terminal

3. Clone this repository: `git clone git@github.com:devbret/HIBP-API-tools.git`

4. Navigate to the repo's directory: `cd HIBP-API-tools`

5. Create a virtual environment: `python3 -m venv venv`

6. Activate your virtual environment: `source venv/bin/activate`

7. Install the needed dependencies: `pip install -r requirements.txt`

8. Run a Python script with the appropriate command: `python3 breach_watch.py`

9. The results will be returned to you in your terminal

10. When finished, exit the virtual environment: `deactivate`

## Other Considerations

This project repo is intended to demonstrate an ability to do the following:

- Provide a command-line toolkit of Python scripts which integrate with the "Have I Been Pwned" API to perform breach intelligence lookups

- Check individual emails, multiple emails, domains and passwords against known data breaches

- Support OSINT workflows through features like retry logic, exponential backoff, JSON output and persistent state files

- Demonstrate secure API integration patterns for identifying exposed credentials and compromised assets

All but one of the Python scripts in this repo require a HIBP API key in order to send and receive data. For more information, please visit [the HaveIBeenPwned website](https://haveibeenpwned.com/API/Key). Otherwise, if you have any questions or would like to collaborate, please reach out either on GitHub or via [my website](https://bretbernhoft.com/).
