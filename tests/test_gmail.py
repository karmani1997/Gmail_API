import unittest
from unittest.mock import Mock
import base64
from dotenv import load_dotenv
load_dotenv()


import os
admin_email = os.environ.get('ADMIN_EMAIL');



class TestEmail(unittest.TestCase):

    def setUp(self):
        # Create a mock service object for the Gmail API
        self.service = Mock()

        # Create an instance of the EmailSender class and set the mock service object
        from gmail_api.gmail import Gmail
        self.email_sender = Gmail()
        self.email_sender.service = self.service

    def test_create_message(self):
        to = admin_email
        subject = "Test Email"
        body = "This is a test email."
        
        expected_result = {
            'raw': 'RnJvbTogWW91ciBOYW1lIDxtZWh0YWIua2FybWFuaUBnbWFpbC5jb20-DQpUbzogbWVodGFiLmthcm1hbmlAZ21haWwuY29tDQpTdWJqZWN0OiBUZXN0IEVtYWlsDQoNClRoaXMgaXMgYSB0ZXN0IGVtYWlsLg=='
        }
        result = self.email_sender.create_message(to, subject, body)

        self.assertEqual(result['raw'], expected_result['raw'])

    def test_send_email(self):
        to = admin_email
        subject = "Test Email"
        body = "This is a test email."

        # Define the expected email message
        expected_message = {
            'raw': 'RnJvbTogWW91ciBOYW1lIDxtZWh0YWIua2FybWFuaUBnbWFpbC5jb20-DQpUbzogbWVodGFiLmthcm1hbmlAZ21haWwuY29tDQpTdWJqZWN0OiBUZXN0IEVtYWlsDQoNClRoaXMgaXMgYSB0ZXN0IGVtYWlsLg=='
        }

        # Set the return value for the Gmail API send method
        self.service.users().messages().send().execute.return_value = {
            "id": "12345"
        }

        # Call the send_email method and check the result
        result = self.email_sender.send_email(to, subject, body)

        self.assertEqual(result, {"id": "12345"})