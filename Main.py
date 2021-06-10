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
        Initialise the constants and gmail api service.
        """
        file = path.dirname(__file__)
        self.CLIENT_SECRET_FILE = path.join(file,'client_secret.json')
        self.API_NAME = 'gmail'
        self.API_VERSION = 'v1'
        self.SCOPES = ['https://mail.google.com/']
        self.service=None

    def auth(self):
        """
        Authinticate the user using OAuth2.0.
        """
        print("in authenticate")
        self.service = Create_Service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)


    def send(self, mail_to,  mail_subject, emailMsg):
        """
        Send Email using GMail API. 

        USAGE:
            mail_to     :   Reciever's email address.
            mail_subject:   Subject of the email.
            emailMsg    :   Message in the email.(Plain Text)
        """
        print("in send mail")
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = mail_to
        mimeMessage['subject'] = mail_subject
        mimeMessage.attach(MIMEText(emailMsg, 'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        message = self.service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        print(message)


#Constants
file = path.dirname(__file__)
CLIENT_SECRET_FILE = path.join(file,'client_secret.json')
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

MAIL_SERVICE=mail() 

def start_client(page_to_load, PORT=8563):
    print("in start client")
    try:
        eel.start(page_to_load, port=PORT)
    except:
        page_to_load = 'get_chrome.html'
        try:
            eel.start(page_to_load,port=PORT, mode='chrome-app')
        except:
            eel.start(page_to_load,port=PORT, mode='edge')

@eel.expose
def token_exists():
    print("In token")
    if path.exists(path.join(file,'token_gmail_v1.pickle')):
        print("Return true")
        return 'True'
    else:
        return 'False'

@eel.expose
def start_without_chrome():
    port = random.randint(5000,8000)
    eel.login_page()

@eel.expose
def authenticate():
    global MAIL_SERVICE
    MAIL_SERVICE.auth()

@eel.expose
def send_mail(mail_to, mail_subject, emailMsg):
    global MAIL_SERVICE
    MAIL_SERVICE.send(mail_to,mail_subject, emailMsg)

if __name__ == '__main__':
    print(" in main")
    port = random.randint(5000,8000)
    start_client('LoginSplash.html', port)