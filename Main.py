from os import path, error
import eel
import random
from pkg import mail
import quopri
from email.header import Header, decode_header, make_header
import re


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
    Checks if the token already exists (User has logged in before). 

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
def get_ids(query="in:inbox", user_id='me'):
    global MAIL_SERVICE
    return MAIL_SERVICE.search_message(query, user_id)


@eel.expose
def get_mail_header(msg_id, user_id='me'):
    global MAIL_SERVICE
    
    mime_element = MAIL_SERVICE.get_mime(msg_id, user_id)
    mail_subject, sender, reciever, sender = (None for i in range(4))

    try:
        mail_subject=mime_element['subject']
    except:
        pass

    try:
        sender = mime_element['from']
    except:
        pass
    try:
        reciever = mime_element['to']
    except:
        pass
    
    try:
        sender=sender.replace('"', '')
    except:
        pass
    try:
        reciever=reciever.replace('"', '')
    except:
        pass

    return {
        'subject': str(Header(str(mail_subject))),
        'from': sender,
        'to': reciever
    }

@eel.expose
def get_mail_body(msg_id):

    print("in get_mail_body")

    mime_element = MAIL_SERVICE.get_mime(msg_id)
    body=MAIL_SERVICE.mail_body(mime_element)
    if body is None:
        try:
            body = mime_element.get_payload()[0].get_payload()
        except:
            body = mime_element.get_payload()
    sender = mime_element['from']
    reciever = mime_element['to']
    mail_subject=mime_element['subject']
    try:
        for char in sender:
            sender=sender.replace('\"', "")
    except:
        pass
    try:
        for char in reciever:
            reciever=reciever.replace('\"', "")
    except:
        pass
    mail_contents = {
        'headers': {
            'subject': str((make_header(decode_header(mail_subject)))),
            'from': sender,
            'to': reciever
        },
        'body': body
    }

    return mail_contents

@eel.expose
def theme_read():
    f = open("theme.json", 'r')
    return f.read()

@eel.expose
def theme_write(theme_json):
    f = open("theme.json", 'w')
    f.write(theme_json)

if __name__ == '__main__':
    print(" in main")
    port = random.randint(5000, 8000)
    start_client('LoginSplash.html', port)
