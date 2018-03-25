#/usr/local/bin/python3
from flask import Flask, jsonify, request
import uuid
import pg8000
from DB import ContactDB

app = Flask(__name__)

contactDB = ContactDB()

@app.route('/health/check')
def healthCheck():
    return jsonify({'status': 'OK'}),200

@app.route('/api/v1.0/contacts', methods=['POST'])
def create_contact():
    contactId  = contactDB.create( request.json["firstName"],request.json["lastName"],request.json["phone"]) 
    return  jsonify({'contactId': contactId}), 201

@app.route('/api/v1.0/contacts/<contactId>', methods=['GET'])
def get_contact(contactId):
    contact  = contactDB.get( contactId) 
    return  jsonify(contact), 200
    
if __name__ == '__main__':
    contactDB.createContactTable()
    app.run(debug=True,host='0.0.0.0')