#/usr/local/bin/python3
from flask import Flask, jsonify, request
from DB import ContactDB,GroupDB
import json
import time
from httplib2 import Http
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

contactDB = ContactDB()
groupDB   = GroupDB()

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

@app.route('/health/check')
def healthCheck():
    return jsonify({'status': 'OK'}),200

@app.route('/api/v1.0/contacts', methods=['POST'])
def create_contact():
    contactId  = contactDB.create( request.json["firstName"],request.json["lastName"],request.json["phone"], request.json("groupId")) 
    return  jsonify({'contactId': contactId}), 201

@app.route('/api/v1.0/contacts/<contactId>', methods=['GET'])
def get_contact(contactId):
    contact  = contactDB.get( contactId) 
    return  jsonify(contact), 200

@app.route("/api/v1.0/contacts", methods=['GET'])
def get_all_contacts():
   contacts =  contactDB.getAll()
   return jsonify(contacts), 200    

@app.route("/api/v1.0/groups", methods=['GET'])
def get_all_groups():
   groups =  groupDB.getAll()
   return jsonify(groups), 200    

@app.route('/api/v1.0/contacts/groups/<groupId>', methods=['GET'])
def get_contact_by_group(groupId):
    contacts  = contactDB.getAllByGroupId( groupId ) 
    return  jsonify(contacts), 200  

@app.route('/api/v1.0/contacts/groups/<groupId>/notify', methods=['POST'])
def post_contact_by_group(groupId):
   
    for contact in contactDB.getAllByGroupId( groupId ): 
         app.logger.info("Attempting to notify contact: {} {}".format(contact["firstName"],
                                                                      contact["lastName"]))
         time.sleep(4)
         contactBody = json.dumps({"contacts": [contact]})
        
         http_obj = Http(".cache")
         (resp, content) = http_obj.request(uri="http://notifier:5010/api/v1.0/notify",method='POST',body=contactBody, headers={'Content-type': 'application/json'})

         if (resp.status==200):
           app.logger.info("Retrieved content back from: {}".format(content.decode("utf-8")))
         else:
           print("Error encountered when looking up contact data.  No data returned")
    
    return  jsonify([]), 200  

@app.route('/api/v1.0/contacts/seed', methods=['POST'])
def post_load_seed_data():
    loadSeedData()
    
    return  jsonify([]), 200  


def loadSeedData():
    groupId = groupDB.create("Telstra Financial Services 401K Managers", "Call Center Managers")
    contactId = contactDB.create("John", "Carnell", "19202651560", groupId)
    contactId = contactDB.create("Christopher", "Carnell", "19842425143", groupId) 


    groupId2 = groupDB.create("Schneider Trucking", "Schneider Trucking Executive Leadership Group")
    contactId = contactDB.create("Mike", "Mckhehan", "19202651555", groupId2)
    contactId = contactDB.create("Dan", "Goerdt", "19202652322", groupId2) 

if __name__ == '__main__':
    contactDB.createContactTable()
    groupDB.createGroupTable()
    app.run(debug=True,host='0.0.0.0')