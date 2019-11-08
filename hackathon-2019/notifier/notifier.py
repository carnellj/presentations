#/usr/local/bin/python3
from flask import Flask, jsonify, request
from twilio.rest import Client
from urllib.parse import quote
import time
import logging
import utils
import log
import sys
import os
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
app = Flask(__name__)

account_sid = ""
auth_token  = ""
   
def get_secret(secret_name):
    try:
        with open('/run/secrets/{0}'.format(secret_name), 'r') as secret_file:
            return secret_file.read()
    except IOError:
        return None

def sendVoiceCall(fromPhoneNumber, toPhoneNumber, firstName, lastName,msgText):
   client = Client(account_sid, auth_token)
   msg=quote(msgText,safe='')
   call = client.calls.create(
    to=toPhoneNumber,
    from_=fromPhoneNumber,
    url="https://handler.twilio.com/twiml/EHf4b0efd9b7ea4c7c3531baf5ff88e9a3?firstName={}&lastName={}&msgText='{}'".format(firstName,lastName,msg))

    
@app.route('/health/check')
def healthCheck():
    return jsonify({'status': 'OK'}),200

@app.route('/api/v1.0/notify', methods=['POST'])
def notify():
  contacts = request.json["contacts"]
 
  for contact in contacts:
     logger.info("Received a request to notify {} {} at {} with message {}.".format(
       contact["firstName"],
       contact["lastName"],
       contact["phoneNumber"],
       contact["msgText"]))  

     firstName   = contact["firstName"]
     lastName    = contact["lastName"]
     phoneNumber = "+{}".format(contact["phoneNumber"])
     msgText     = contact["msgText"]
     message     = "Hi {} {}.  {}".format(firstName,lastName,msgText)  
     client = Client(account_sid, auth_token)
     message = client.api.account.messages.create(
       to=phoneNumber,
       from_='+19206541198',
       body=message)
   
     sendVoiceCall('+19206541198',phoneNumber,firstName,lastName,msgText)
     return jsonify({"status": "call successful"}),200    

if __name__ == '__main__':
   account_sid = os.environ["TWILIO_SID"]
   auth_token  = os.environ["TWILIO_TOKEN"]
   app.run(debug=True,host='0.0.0.0', port=5010)

    