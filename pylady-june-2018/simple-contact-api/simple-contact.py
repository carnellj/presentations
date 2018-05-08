#/usr/local/bin/python3
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)
contacts = {}

@app.route('/health/check')
def healthCheck():
    return jsonify({'status': 'OK'}),200

@app.route('/api/v1.0/contacts', methods=['POST'])
def create_contact():
    contactId  = str(uuid.uuid4())
    contact = {"contactId": contactId, 
               "firstName":request.json["firstName"],
               "lastName": request.json["lastName"],
               "phone":    request.json["phone"]}
    contacts["contactId"] = contact
    return  jsonify(contact), 201

@app.route('/api/v1.0/contacts/<contactId>', methods=['GET'])
def get_contact(contactId):
    if "contactId" in contacts:
      contact  = contacts["contactId"] 
      return  jsonify(contact), 200
    else:
        return jsonify({}), 404

@app.route('/api/v1.0/contacts/<contactId>', methods=['DELETE'])
def delete_contact(contactId):
    if "contactId" in contacts:
      del(contacts["contactId"]) 
      return  jsonify({}), 200
    else:
        return jsonify({}), 404      

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5001)