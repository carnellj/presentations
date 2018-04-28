#/usr/local/bin/python3
from flask import Flask, jsonify, request
from twilio.rest import Client
import urllib
import urllib3
import time
import cgi
import logging
import sys
from logging.handlers import RotatingFileHandler


app = Flask(__name__)

account_sid = ""

auth_token  = ""

@app.before_first_request
def initialize_logging():
    if not app.debug:
        print('Setting up logging...')
 
        # Get the apps logging level or default to INFO
        log_level = app.config.get('LOGGING_LEVEL')
        if not log_level:
            log_level = logging.INFO
 
        # Set up default logging for submodules to use STDOUT
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
 
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
 
        # Remove the Flask default handlers and use our own
        del app.logger.handlers[:]
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')

   
def get_secret(secret_name):
    try:
        with open('/run/secrets/{0}'.format(secret_name), 'r') as secret_file:
            return secret_file.read()
    except IOError:
        return None

def sendVoiceCall(fromPhoneNumber, toPhoneNumber, firstName, lastName):
   client = Client(account_sid, auth_token)
   ts = time.gmtime()
   url="https://handler.twilio.com/twiml/EHf4b0efd9b7ea4c7c3531baf5ff88e9a3?firstName={}&lastName={}&appointment='{}'".format(firstName,lastName, urllib.parse.quote_plus(time.strftime("%c", ts), safe='', encoding=None, errors=None))
   call = client.calls.create(
    to=toPhoneNumber,
    from_=fromPhoneNumber,
    url="https://handler.twilio.com/twiml/EHf4b0efd9b7ea4c7c3531baf5ff88e9a3?firstName={}&lastName={}&appointment='{}'".format(firstName,lastName,url))

    
@app.route('/health/check')
def healthCheck():
    return jsonify({'status': 'OK'}),200

@app.route('/api/v1.0/notify', methods=['POST'])
def notify():
  contacts = request.json["contacts"]
  for contact in contacts:
     firstName   = contact["firstName"]
     lastName    = contact["lastName"]
     phoneNumber = "+{}".format(contact["phoneNumber"])
     message     = "Hi {} {}.  Your appointment is upcoming".format(firstName,lastName)  
     app.logger.info("ACCOUNT_SID {}".format(account_sid))
     client = Client(account_sid, auth_token)
     message = client.api.account.messages.create(
       to=phoneNumber,
       from_='+19206541198',
       body=message)
   
     sendVoiceCall('+19206541198',phoneNumber,firstName,lastName)
     return "ok"
     #print(message.sid)     

if __name__ == '__main__':
   account_sid = get_secret("account_sid")
   auth_token  = get_secret("auth_token")
   app.run(debug=True,host='0.0.0.0', port=5010)

    