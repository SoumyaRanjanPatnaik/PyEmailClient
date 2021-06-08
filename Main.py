from functools import total_ordering
import os
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import path
import eel
import random

#Constants
file = path.dirname(__file__)
CLIENT_SECRET_FILE = path.join(file,'client_secret.json')
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

eel.init('Static')

def token_exists():
    print("In token")
    if path.exists(path.join(file,'token_gmail_v1.pickle')):
        return True
    else:
        return False

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
def authenticate():
    print("in authenticate")
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    return service

@eel.expose
def start_without_chrome():
    port = random.randint(5000,8000)
    if token_exists():
        eel.main_page()
    else:
        eel.login_page()

@eel.expose
def send_mail(mail_to,  mail_subject, emailMsg):
    service = authenticate()
    print("in send mail")
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = mail_to
    mimeMessage['subject'] = mail_subject
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(message)


if __name__ == '__main__':
    print(" in main")
    port = random.randint(5000,8000)
    if token_exists():
        start_client('index.html', port)
    else:
        start_client('LoginSplash.html', port)