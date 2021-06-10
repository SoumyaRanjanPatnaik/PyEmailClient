# PyEmailClient

---

**_PyMail_**(_PyEmailClient_) is fully functional, cross-platform Email Client for sending and browsing emails, written in Python. It only works for gmail accounts for now.

# Usage:

---

This app requires a chromium-based browser or chrome for the best experience. But the app can be opened in a browser as a web-app

## Login:

You can log into the software by using OAuth2.0. Upon opnening PyMail, you will see the login page. On clicking the login button, you will be redirected to the google authentication page. On successful authentication, a token file by the name of _token_gmail_v1.pickle_ will be generated to keep the user logged-in.

**_NOTE_**: Do **_NOT_** share the token file (token_gmail_v1.pickle) with anyone. Doing so will allow anyone to access your GMail account.

## Compose:

## Search for mails:

## Navigate folders/lables.

## Read mail.

## Add attatchments.

## Save mail to draft.

# Developer's Guide

---

To setup the project, follow the following steps:

1. Clone the repository into the directory of your choice and open the PyEmailClient directory.
		git clone git@github.com:SoumyaRanjanPatnaik/PyEmailClient.git
		cd PyEmailClient
2. Download and install anaconda if not already installed. Visit https://conda.io/projects/conda/en/latest/user-guide/install/index.html to download it for your operating sytem. If you are on linux/MacOS, you can also intall it using the package manager included with your distro or HomeBrew (Mac Users only).
3. Setup and activate anaconda environment.
		conda env create -f environment.yml
		conda activate EmailClient
This will install all the required libraries and dependencies required for running PyMail inside the environment '*EmailClient*' and activate it. You are all set for reviewing the codebase, making changes and contributing to this repository. 
4. To run the program, first make sure that you are inside the *EmailClient* anaconda environment. Then run the *Main.py* python file.
		python Main.py
The application should automatically open up.
5. To build the distributable PyMail application, execute the *build.sh* bash-script in your shell from the root directory of the project if you're in linux or Max. Mac users make sure you have bash shell installed in their terminal. 
		./build.sh
A *build.bat* file will soon be added to this repository, which will allow for easily building PyMail from winows. 

Alternatively, you can run the following command
		python -m eel Main.py Static --add-data "client_secret.json:." --add-data "token_gmail_v1.pickle:." --noconsole
Make sure you have a *client_secret.json* file and *toke_gmail_v1.pickle* file before building. If it is not present, you can crerate blank files with the above mentioned file names too.
		touch token_gmail_v1.pickle
		touch client_secret.json
6. To view your distributable, open the dist/Main directory and open Main or Main.exe(in case of windows).
