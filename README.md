## GMAIL API SETUP

To set up a connection with the Gmail API, you need to follow these steps:

* Create a Google Cloud Platform project: Go to the Google Cloud Console and create a new project. Once you have created the project, enable the Gmail API in the API Library.
* Create API credentials: In the Google Cloud Console, create a set of API credentials for your project. Select the "OAuth client ID" option, choose "Desktop app" as the application type, and give the credentials a name. This will create a client ID and client secret that you will use in your Python code.
* Install the Google client library: In order to interact with the Gmail API from Python, you need to install the Google client library. You can install it using pip by running the following command:
pip install google-api-python-client
* Authorize the API client: You need to authorize your Python code to access your Gmail account. To do this, use the credentials you created in step 2 to authenticate the client. You can do this by following the steps in the Google OAuth2 documentation.
* Use the Gmail API: Once you have authorized the API client, you can start using the Gmail API in your Python code. You can use the Google client library to make requests to the API and retrieve information about your email account, such as the list of messages, labels, and attachments.
    

# Description of the Project

In this task I have implemented the gmail_api in python with two main functionalities **send email** and search the emails against the **keywords**,
with the front-end in flask api so that user can send the email from webpage and search the emails against the keywords.
* Gmail
> 	This is the main class of the api in which implement three functions authenticate_google_api, create_message, send_email and search_emails_with_keywords, 
	authenticate_google_api : read the authentication from json and create gmail api client to send and read the email
	create_message: create the encoded email.
	send_email : send the email using gmail_api_client create_message method and  return the success or failure
	search_emails_with_keywords: return the list of dict of emails against the keywords.


# How to run the project and test cases	

* Install requirement.txt file
* Install the requirements.txt using the following command 

	```
	pip3 install -r requirements.txt 
	```


* Run the project to send and get the emails

	```
	python3 app.py
```
* Run the test cases
```
	python3 -m unittest tests.test_gmail
```






