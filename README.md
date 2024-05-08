# HaveIBeenPwned API Tools
Python scripts for interfacing with the HaveIBeenPwned API via the CLI.

All but one of the Python scripts in this repo require a HIBP API key in order to send and receive data. For more information, please visit [the HaveIBeenPwned website](https://haveibeenpwned.com/API/Key).

## Set Up

### Programs Needed 

- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/) (When installing on Windows, make sure you check the ["Add python 3.xx to PATH"](https://hosting.photobucket.com/images/i/bernhoftbret/python.png) box.)

### Steps

1. Install the above programs.
2. Open a shell window (For Windows open PowerShell, for MacOS open Terminal & for Linux open your distro's terminal emulator).
3. Clone this repository using `git` by running the following command; `git clone https://github.com/devbret/HIBP-API-tools`.
4. Navigate to the repo's directory by running; `cd HIBP-API-tools`.
5. Install the needed dependencies for running the script by running; `pip install -r requirements.txt`.
6. In a text editor of your choice, edit the appropriate value(s) with your HIBP API key, for any of the Python scripts that you choose to run.
7. Run a selected script with the command `python3 example_python_script_name.py`.
8. The results will be returned to you in your terminal.
