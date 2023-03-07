"""
File: gmail.py
--------------
Gmail Class service object. Currently supports sending mail 
and retrieving mails with the keywords in the emails.
"""

#import packages
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup
import json
import os
import base64
from dotenv import load_dotenv
load_dotenv()

admin_email = os.environ.get('ADMIN_EMAIL');



class Gmail(object):
  
    def __init__(self):
        # Define the scopes for the Gmail API
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']
        self.credentials = None
        self.data = []
        self.service = None
        self.default_port = 0

    def authenticate_google_api(self):
        """
        This function read the auth_credential from the json file, create token and build Gmail API client
        """
        if self.service is None:
            try:
                # Load credentials from file
                with open('GMAIL_API/credentials/token.json', 'r') as f:
                    credentials_dict = json.load(f)
                    self.credentials = Credentials.from_authorized_user_info(credentials_dict)
                
            except:
                print("Inside")
                """
                Authenticates the Google API using the client ID and secret in the JSON file.
                """
                # Set the path to the client ID JSON file
                CLIENT_SECRET_FILE = 'gmail_api/credentials/auth_credentials_desktop.json'

                # Define the credentials for the OAuth 2.0 flow
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE, self.SCOPES)
                credentials = flow.run_local_server(port = self.default_port)
                # Save the credentials to a file
                with open('gmail_api/credentials/token.json', 'w') as f:
                    json.dump(credentials.to_json(), f)

                self.credentials=credentials

            # Build the Gmail API client
            self.service = build('gmail', 'v1', credentials=self.credentials)


    def create_message(self, to: str, subject: str, body: str) -> dict:
        """
        Creates a message for an email.
        """
        message = (f'From: Your Name <{admin_email}>\r\n'
                f'To: {to}\r\n'
                f'Subject: {subject}\r\n\r\n'
                f'{body}')
        message_bytes = message.encode('utf-8')
        encoded_message = base64.urlsafe_b64encode(message_bytes).decode('utf-8')
        return {'raw': encoded_message}


    def send_email(self, to: str, subject: str, body: str) -> dict:
        """
        Sends an email with the given subject and body to the specified recipient.
        """
        try:
            # Authenticate the Google API
            self.authenticate_google_api()

            # Define the email message
            message = self.create_message(to, subject, body)

            # Send the message using the Gmail API
            send_message = (self.service.users().messages().send(userId="me", body=message)
                            .execute())
            #print(F'Sent message to {to} Message Id: {send_message["id"]}')

        except HttpError as error:
            print(F'An error occurred: {error}')
            send_message = {None}

        return send_message

    def search_emails_with_keywords(self, keywords: str) -> list:
        """
        Searches for emails with the specified keywords in the subject or body.
        """
        self.data = []
        try:
            # Authenticate the Google API
            self.authenticate_google_api()

            # Define the search query
            query = ''
            #for keyword in keywords:
            query += f'subject:{keywords} OR '
            query += f'body:{keywords} OR '
            query = query[:-4]  # Remove the last ' OR '

            # Search for emails matching the query
            messages = self.service.users().messages().list(userId='me', q=query).execute().get('messages', [])

            # the subject, from and body of each matching email
            for message in messages:
    
                msg = self.service.users().messages().get(userId='me',id=message['id']).execute()
                #print (msg)
                subject = [header['value'] for header in msg['payload']['headers']
                        if header['name'] == 'Subject'][0]
                From = [header['value'] for header in msg['payload']['headers']
                        if header['name'] == 'From'][0]
                snippet = msg['snippet']
                self.data.append({'subject':subject, 'msg':snippet, 'From':From})


        except HttpError as error:
            print(F'An error occurred: {error}')
            messages = []
        #print (self.data)
        return self.data
    
