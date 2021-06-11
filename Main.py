from functools import total_ordering
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors
from os import path, error
import eel
import random
import email


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

    def search_message(self, search_string='in:inbox', user_id='me'):
        """
        Search the inbox for emails using standard gmail search parameters
        and return a list of email IDs for each result
        PARAMS:
            search_string(default='in:inbox'): search operators you can use with Gmail
            (see https://support.google.com/mail/answer/7190?hl=en for a list)
            user_id (default='me'): user id for google api service ('me' works here if
            already authenticated)
        RETURNS:
            List containing email IDs of search query
        """
        try:
            # initiate the list for returning
            list_ids = []

            # get the id of all messages that are in the search string
            search_ids = self.service.users().messages().list(userId=user_id, q=search_string).execute()
            
            # if there were no results, print warning and return empty string
            try:
                ids = search_ids['messages']

            except KeyError:
                print("WARNING: the search queried returned 0 results")
                print("returning an empty string")
                return [""]

            if len(ids)>1:
                for msg_id in ids:
                    list_ids.append(msg_id['id'])
                return list_ids

            else:
                list_ids.append(ids['id'])
                return list_ids
            
        except (errors.HttpError, error):
            print("An error occured: %s") % error

    def get_mime(self, msg_id, user_id ='me' ):
        """
        Search the inbox for specific message by ID and return it back as a 
        clean string. String may contain Python escape characters for newline
        and return line. 
        
        PARAMS
            msg_id: the unique id of the email you need
            user_id(default = 'me'): user id for google api service ('me' works here if
            already authenticated)
        RETURNS
            A string of encoded text containing the message body
        """
        try:
            # grab the message instance
            message = self.service.users().messages().get(userId=user_id, id=msg_id,format='raw', metadataHeaders=None).execute()

            # decode the raw string, ASCII works pretty well here
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

            # grab the string from the byte object
            mime_msg = email.message_from_bytes(msg_str)
            
            return mime_msg
        except Exception:
            pass

    def mail_body( self, mime_msg):
        try:
            # check if the content is multipart (it usually is)
            content_type = mime_msg.get_content_maintype()
            if content_type == 'multipart':
                # there will usually be 2 parts the first will be the body in text
                # the second will be the text in html
                parts = mime_msg.get_payload()

                # return the encoded text
                final_content = parts[0].get_payload()
                print("\n\n"+final_content)
                return final_content

            elif content_type == 'text':
                return mime_msg.get_payload()

            else:
                print("\nMessage is not text or multipart, returned an empty string")
                return ""
        except Exception:
            pass


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


if __name__ == '__main__':
    print(" in main")
    port = random.randint(5000, 8000)
    start_client('LoginSplash.html', port)