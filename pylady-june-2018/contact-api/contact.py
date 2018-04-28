#/usr/local/bin/python3
from flask import Flask, jsonify, request
from DB import ContactDB,GroupDB

app = Flask(__name__)

contactDB = ContactDB()
groupDB   = GroupDB()

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

def loadSeedData():
    groupId = groupDB.create("Telstra Financial Services 401K Managers", "Call Center Managers")
    contactId = contactDB.create("John", "Carnell", "9202651560", groupId)
    contactId = contactDB.create("Liz", "Patterson", "9202651560", groupId) 

    groupId2 = groupDB.create("Schneider Trucking", "Schneider Trucking Executive Leadership Group")
    contactId = contactDB.create("Mike", "Mckhehan", "9202651555", groupId2)
    contactId = contactDB.create("Dan", "Goerdt", "9202652322", groupId2) 

if __name__ == '__main__':
    contactDB.createContactTable()
    groupDB.createGroupTable()
    loadSeedData()
    app.run(debug=True,host='0.0.0.0')