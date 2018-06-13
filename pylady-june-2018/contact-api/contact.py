#/usr/local/bin/python3
from flask import Flask, jsonify, request
from DB import ContactDB,GroupDB
import json
import time
from httplib2 import Http
import logging
import utils
import log
import os

logger = logging.getLogger(__name__)
app = Flask(__name__)

#@app.before_first_request
def init_app():
    logger.info("Initializing the contact service.")
    global contactDB
    global groupDB
    logger.info("User: {}".format(os.environ["POSTGRES_USER"]))
    logger.info("DB: {}".format( os.environ["POSTGRES_DB"]))
    logger.info("HOST: {}".format( os.environ["POSTGRES_HOSTNAME"]))
    logger.info("Creating the contact db connection")
    contactDB = ContactDB(os.environ["POSTGRES_USER"],
                             os.environ["POSTGRES_PASSWORD"],
                             os.environ["POSTGRES_DB"],
                             os.environ["POSTGRES_HOSTNAME"]  )
    logger.info("Creating the groupdb connection")            
    groupDB = GroupDB(   os.environ["POSTGRES_USER"],
                             os.environ["POSTGRES_PASSWORD"],
                              os.environ["POSTGRES_DB"],
                             os.environ["POSTGRES_HOSTNAME"]  )  
    logger.info("Creating the contact db table")                      
    contactDB.createContactTable()
    logger.info("Creating the Group db table")         
    groupDB.createGroupTable()  

@app.after_request
def per_request_callbacks(response):
    response.headers['tmx-correlation-id']=str(utils.request_id())
    return response                            

@app.route('/health/check')
def healthCheck():
    return jsonify({'status': 'OK'}),200

@app.route('/api/v1.0/contacts', methods=['POST'])
def create_contact():
    logger.debug("Creating a contact record:  FirstName: {}. LastName: {}. Phone {}. Group Id {}".format(request.json["firstName"],request.json["lastName"],request.json["phone"], request.json["groupId"]))

    contactId  = contactDB.create( request.json["firstName"],request.json["lastName"],request.json["phone"], request.json["groupId"]) 
    return  jsonify({'contactId': contactId}), 201

@app.route('/api/v1.0/contacts/<contactId>', methods=['GET'])
def get_contact(contactId):
    logger.debug("Retrieve contact {} from database.".format(contactId))
    contact  = contactDB.get( contactId) 
    return  jsonify(contact), 200

@app.route("/api/v1.0/contacts", methods=['GET'])
def get_all_contacts():
   logger.debug("Retrieving al contacts in the database") 
   contacts =  contactDB.getAll()
   return jsonify(contacts), 200    

@app.route("/api/v1.0/groups", methods=['GET'])
def get_all_groups():
   logger.info("Retrieving all groups from the /api/v1.0/groups method")
   groups =  groupDB.getAll()
   return jsonify(groups), 200    

@app.route('/api/v1.0/contacts/groups/<groupId>', methods=['GET'])
def get_contact_by_group(groupId):
    logger.debug("Retrieving all contacts belong to group {}.".format(groupId))
    contacts  = contactDB.getAllByGroupId( groupId ) 
    return  jsonify(contacts), 200  

@app.route('/api/v1.0/contacts/groups/<groupId>/notify', methods=['POST'])
def post_contact_by_group(groupId):
    text = request.json["msgText"]
    for contact in contactDB.getAllByGroupId( groupId ): 
         logger.info("Attempting to notify contact: {} {} with message {}".format(contact["firstName"],
                                                                                   contact["lastName"],
                                                                                   text ))
         contact["msgText"] = text
         contactBody = json.dumps({"contacts": [contact]})
         
        
         http_obj = Http(".cache")
         (resp, content) = http_obj.request(uri="http://notifier:5010/api/v1.0/notify"
              ,method='POST',body=contactBody, headers={'Content-type': 'application/json',
                                                        'tmx-correlation-id': str(utils.request_id())})

         if (resp.status==200):
           app.logger.info("Retrieved content back from: {}".format(content.decode("utf-8")))
         else:
           print("Error encountered when looking up contact data.  No data returned")
    
    return  jsonify([]), 200  

@app.route('/api/v1.0/contacts/seed', methods=['POST'])
def post_load_seed_data():
    logger.info("Loading the seed data into the database")
    loadSeedData()
    
    return  jsonify([]), 200  

def loadSeedData():
    init_app()
    logger.info("Loading the first piece of group data.")
    groupId = groupDB.create("Telstra Financial Services 401K Managers", "Call Center Managers")
    contactId = contactDB.create("John", "Carnell", "19202651560", groupId)
    contactId = contactDB.create("Christopher", "Carnell", "19842425143", groupId)

    logger.info("Loading the second piece of group data.")
    groupId2 = groupDB.create("Schneider Trucking", "Schneider Trucking Executive Leadership Group")
    contactId = contactDB.create("Mike", "Mckhehan", "19202651555", groupId2)
    contactId = contactDB.create("Dan", "Goerdt", "19202652322", groupId2) 

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')