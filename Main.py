from functools import total_ordering
import os
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import path
import eel
import random


eel.init('Static')


class mail:
    """
    Class containing necessary functions for interacting with google API.
    """

    def __init__(self):
        """
        Constructor of class 'mail'. Initialises the necessary constants.
        """
        file = path.dirname(__file__)
        self.CLIENT_SECRET_FILE = path.join(file, 'client_secret.json')
        self.API_NAME = 'gmail'
        self.API_VERSION = 'v1'
        self.SCOPES = ['https://mail.google.com/']
        self.service = None

    def auth(self):
        """
        Authinticate the user using OAuth2.0.

        RETURNS: None
        """
        print("in authenticate")
        self.service = Create_Service(
            self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)

    def send(self, mail_to,  mail_subject, emailMsg):
        """
        Send Email using GMail API. 

        PARAMS:
            mail_to     :   Reciever's email address.
            mail_subject:   Subject of the email.
            emailMsg    :   Message in the email.(Plain Text)

        RETURNS: None
        """
        print("in send mail")
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = mail_to
        mimeMessage['subject'] = mail_subject
        mimeMessage.attach(MIMEText(emailMsg, 'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        message = self.service.users().messages().send(
            userId='me', body={'raw': raw_string}).execute()
        print(message)

    def get_labels(self):
        """
        Get labels of the user. Labels are the folders into which the 
        mail is categorised. This also includes the folders/labels
        created by the user for their Gmail account.

        RETURNS: 
        A dictionary with two elements:

            1. 'imp':   The value of this key contains the most used labels.

            2. 'other': The value of this key contains the labels that indicate categories (like updates, promotions, social, etc)
        """
        print('in labels')
        service = authenticate()
        results = self.service.users().labels().list(userId='me').execute()
        labels_details = results.get('labels', [])
        labels = []
        others = []
        for i in labels_details:
            if 'CATEGORY' in i['name']:
                others.append(i['name'].replace("CATEGORY_", ""))
            else:
                labels.append(i['name'])
        return {'imp': labels, 'other': others}


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
    except:
        page_to_load = 'get_chrome.html'
        try:
            eel.start(page_to_load, port=PORT, mode='chrome-app')
        except:
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


if __name__ == '__main__':
    print(" in main")
    port = random.randint(5000, 8000)
    start_client('LoginSplash.html', port)
