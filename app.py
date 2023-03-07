from flask import Flask, request
import webbrowser
from gmail_api.gmail import Gmail
from flask import Flask, request,render_template



#Gmail Object to intract with GMAIL_API
gmail_obj = Gmail()
#Flask Object
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    """
    This function get the email_id, subject and msg from the webpage and send the data to GMAIL_API 
    """
    if request.method == 'POST':
        sender_gmail = request.form['sender_gmail']
        subject_gmail = request.form['subject_gmail']
        body_gmail = request.form['body_gmail']

        gmail_obj.send_email(str(sender_gmail), str(subject_gmail), str(body_gmail))
        return 'email sent successfully..'
    else:
        return render_template('send_email.html')

@app.route('/search_keywords', methods=['GET', 'POST'])
def search_keywords():
    """
    This function get the keywords from the webpage and show gmails data against the keyword and show it on the webpage
    """
    if request.method == 'POST':
        search_keywords = request.form['key_words']
        print (search_keywords)
        data = gmail_obj.search_emails_with_keywords(str(search_keywords))

        return render_template('email_data.html', data={'data' : data, 'keyword' : search_keywords})
        #send_email(sender_gmail, subject_gmail, body_gmail)
        #return 'email sent successfully..'
    else:
        return render_template('search_keywords.html')


if __name__ == '__main__':
    """
    To start the flask service open the webpage on the browser and run the service on the localhost with port 2000
    """
    webbrowser.open_new('http://127.0.0.1:3000/')
    app.run(host="0.0.0.0", port=3000)
