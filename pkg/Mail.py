from email.header import decode_header, make_header
from functools import total_ordering
from typing import final
from pkg.Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors
from os import path, error
import email
from email import policy
import quopri

class mail:
    """
    Class containing necessary functions for interacting with google API.
    """

    def __init__(self):
        """
        Constructor of class 'mail'. Initialises the necessary constants.
        """
        file = path.dirname(__file__)
        self.CLIENT_SECRET_FILE = path.join(path.dirname(file), 'client_secret.json')
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
        A list containing multiple dictionaries containing details about the labels.
        """
        print('in labels')
        results = self.service.users().labels().list(userId='me').execute()
        return results.get('labels', [])

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
            
            ids={}

            # if there were no results, print warning and return empty string
            try:
                ids = search_ids['messages']

            except KeyError:
                print("WARNING: the search queried returned 0 results")
                print("returning an empty string")
                return []

            if len(ids)>1:
                for msg_id in ids:
                    list_ids.append(msg_id['id'])
                return list_ids

            else:
                list_ids.append(ids[0]['id'])
                return list_ids
            
        except (errors.HttpError, error):
            print("An error occured: %s") % error

    def get_mime(self, msg_id, user_id ='me' ):
        """
        Search the inbox for specific message by ID and return it back as a 
        MIME object. The MIME object may contain "subject", "from", "to", 
        and the mail body along with some metadata. 
        
        PARAMS
            msg_id: the unique id of the email you need
            user_id(default = 'me'): user id for google api service ('me' works here if
            already authenticated)
        RETURNS
            Mail in form of MIME element.
        """
        try:
            # grab the message instance
            message = self.service.users().messages().get(userId=user_id, id=msg_id,format='raw', metadataHeaders=None).execute()

            # decode the raw string, UTF-8 works pretty well here
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('UTF-8'))

            mime_msg = email.message_from_bytes(msg_str,policy=policy.default)
            return mime_msg
        except Exception:
            pass

    def mail_body( self, mime_msg=None):
        """
            Takes MIME object as the only parameter and returns
            the body of the message.

            PARAMS:
                mime_msg: MIME type containing the data of the email.
            
            RETURNS:
                The body of the message as string in plain text. The string
                might contain escape characters for new line and return.
        """
        try:
            # check if the content is multipart (it usually is)
            content_type = mime_msg.get_content_maintype()

            if content_type == 'multipart':
                # there will usually be 2 parts the first will be the body in text
                # the second will be the text in html
                parts = mime_msg.get_payload()

                # return the encoded text
                final_content = quopri.decodestring(parts[1].get_payload()).decode('utf-8')
                print("\n\n"+final_content)
                return final_content

            elif content_type == 'text':
                return quopri.decode(mime_msg.get_payload()).decode('utf-8')

            else:
                print("\nMessage is not text or multipart, returned an empty string")
                return ""
        except Exception:
            pass
