from functools import total_ordering
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import path
import eel
import random

#Constants
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

eel.init('Static')

def token_exists():
    if path.exists('./token_gmail_v1.pickle'):
        return True
    elif path.exists('.\\token_gmail_v1.pickle'):
        return True
    else:
        return False

def start_client(page_to_load, PORT=8563):
    try:
        eel.start(page_to_load, port=PORT)
    except:
        page_to_load = 'get_chrome.html'
        try:
            eel.start(page_to_load,port=PORT, mode='chrome-app')
        except:
            eel.start(page_to_load,port=PORT, mode='edge')

    
def authenticate():
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    return service

@eel.expose
def send_mail(mail_to,  mail_subject, emailMsg):
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = mail_to
    mimeMessage['subject'] = mail_subject
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    print(message)


if __name__ == '__main__':
    if token_exists():
        start_client('index.html')
    else:
        start_client('LoginSplash.html')
    service = authenticate()
    