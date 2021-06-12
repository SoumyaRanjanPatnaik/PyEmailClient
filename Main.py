from os import path, error
import eel
import random
from pkg import mail
import email


eel.init('Static')

# Constants
file = path.dirname(__file__)
CLIENT_SECRET_FILE = path.join(file, 'client_secret.json')
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

MAIL_SERVICE = mail()


def start_client(page_to_load, PORT=8563):
    """
    Starts Python-Eel client and loads the page passed in 
    'page_to_load', on port 'PORT'. 

    RETURNS: None
    """
    print("in start client")
    try:
        eel.start(page_to_load, port=PORT)
    except Exception:
        page_to_load = 'get_chrome.html'
        try:
            eel.start(page_to_load, port=PORT, mode='chrome-app')
        except Exception:
            eel.start(page_to_load, port=PORT, mode='edge')


@eel.expose
def token_exists():
    """
    Checks if the token already exists. 

    RETURNS:
    True: If token already exists.
    False: If token doesn't already exist.

    NOTE: This function is exposed to eel, and can be accessed from javascript.
    """
    print("In token")
    if path.exists(path.join(file, 'token_gmail_v1.pickle')):
        print("Return true")
        return 'True'
    else:
        return 'False'


@eel.expose
def start_without_chrome():
    """
    Loads login page if the user chooses to open in browser, if chrome is not installed already. 

    NOTE: This function is exposed to python eel.
    """
    port = random.randint(5000, 8000)
    eel.login_page()


@eel.expose
def authenticate():
    """
    Function to call the MAIL_SERVICE.auth() function from javascript.

    NOTE: This function is exposed to python eel.
    """
    global MAIL_SERVICE
    MAIL_SERVICE.auth()


@eel.expose
def mail_labels():
    """
    Function to call MAIL_SERVICE.get_labels()

    RETURNS: Dictionary with two elements, having labels 'imp' and 'other'

    NOTE: This function is exposed to python eel.
    """
    global MAIL_SERVICE
    return MAIL_SERVICE.get_labels()


@eel.expose
def send_mail(mail_to, mail_subject, emailMsg):
    """
    Function to call MAIL_SERVICE.send()

    PARAMS:
        mail_to     :   Reciever's email address.
        mail_subject:   Subject of the email.
        emailMsg    :   Message in the email.(Plain Text)

    RETURNS: None

    """
    global MAIL_SERVICE
    MAIL_SERVICE.send(mail_to, mail_subject, emailMsg)

@eel.expose
def get_ids():
    pass

@eel.expose
def get_subject():
    pass


if __name__ == '__main__':
    print(" in main")
    port = random.randint(5000, 8000)
    start_client('LoginSplash.html', port)