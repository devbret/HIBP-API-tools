# Have I Been Pwned API Tools

A comprehensive command-line toolkit for interacting with the Have I Been Pwned API, covering individual breach lookups, email breach checks, advanced stealer log queries and more.

## Overview

Together these Python Python programs range from simple interactive scripts to more robust CLI applications featuring retry logic, JSON output options, exponential backoff, persistent state files and structured result handling. Effectively forming a modular OSINT-style breach intelligence suite built around secure API patterns and automation-friendly design.

## Set Up

All but one of the Python scripts in this repo require a HIBP API key in order to send and receive data. For more information, please visit [the HaveIBeenPwned website](https://haveibeenpwned.com/API/Key).

Below are instructions for installing and running this application on a Linux machine.

### Programs Needed

- [Git](https://git-scm.com/downloads)

- [Python](https://www.python.org/downloads/)

### Steps

1. Install the above programs

2. Open a terminal

3. Clone this repository using `git` by running the following command: `git clone git@github.com:devbret/HIBP-API-tools.git`

4. Navigate to the repo's directory by running: `cd HIBP-API-tools`

5. Install the needed dependencies for running the script by running: `pip install -r requirements.txt`

6. Run a selected script with the appropriate command

7. The results will be returned to you in your terminal

## Other Considerations

This project repo is intended to demonstrate an ability to do the following:

- Integrate multiple HIBP API endpoints to monitor breaches, query compromised emails/domains and track stealer log activity

- Reliably automate breach intelligence gathering and reporting

- Perform targeted security checks to enable automated OSINT workflows for identifying exposed credentials and compromised assets

If you have any questions or would like to collaborate, please reach out either on GitHub or via [my website](https://bretbernhoft.com/).
