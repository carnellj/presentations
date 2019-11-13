# /usr/local/bin/python3
from flask import Flask, jsonify, request
from DB import ContactDB, GroupDB, RfidDB, MusicOptionDB
import json
import time
from httplib2 import Http
import logging
import utils
import log
import os
import time

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.before_first_request
def initializeConnections():
    logger.info("Initializing the contact service.  ")
    global contactDB
    global groupDB
    global rfidDB
    global musicOptionDB
    logger.info("User: {}".format(os.environ["POSTGRES_USER"]))
    logger.info("DB: {}".format(os.environ["POSTGRES_DB"]))
    logger.info("HOST: {}".format(os.environ["POSTGRES_HOSTNAME"]))
    logger.info("Creating the contact db connection")
    contactDB = ContactDB(os.environ["POSTGRES_USER"],
                          os.environ["POSTGRES_PASSWORD"],
                          os.environ["POSTGRES_DB"],
                          os.environ["POSTGRES_HOSTNAME"])
    logger.info("Creating the groupdb connection")
    groupDB = GroupDB(os.environ["POSTGRES_USER"],
                      os.environ["POSTGRES_PASSWORD"],
                      os.environ["POSTGRES_DB"],
                      os.environ["POSTGRES_HOSTNAME"])
    logger.info("Creating the rfidDB connection")
    rfidDB = RfidDB(os.environ["POSTGRES_USER"],
                    os.environ["POSTGRES_PASSWORD"],
                    os.environ["POSTGRES_DB"],
                    os.environ["POSTGRES_HOSTNAME"])
    logger.info("Creating the musicoOtiondb connection")
    musicOptionDB = MusicOptionDB(os.environ["POSTGRES_USER"],
                                  os.environ["POSTGRES_PASSWORD"],
                                  os.environ["POSTGRES_DB"],
                                  os.environ["POSTGRES_HOSTNAME"])


def init_app():
    logger.info("Creating the contact db table")
    contactDB.createContactTable()
    logger.info("Creating the Group db table")
    groupDB.createGroupTable()
    logger.info("Creating the RFID db table")
    rfidDB.createRfidUsersTable()
    logger.info("Creating the Music Options db table")
    musicOptionDB.createMusicOptionTable()


@app.after_request
def per_request_callbacks(response):
    response.headers['tmx-correlation-id'] = str(utils.request_id())
    return response


@app.route('/health/check')
def healthCheck():
    return jsonify({'status': 'OK'}), 200


@app.route('/api/v1.0/contacts', methods=['POST'])
def create_contact():
    logger.debug("Creating a contact record:  FirstName: {}. LastName: {}. Phone {}. Group Id {}".format(
        request.json["firstName"], request.json["lastName"], request.json["phone"], request.json["groupId"]))

    contactId = contactDB.create(request.json["firstName"], request.json["lastName"], request.json["phone"],
                                 request.json["groupId"])
    return jsonify({'contactId': contactId}), 201


@app.route('/api/v1.0/rfid', methods=['POST'])
def create_rfidUser():
    logger.debug("Creating a rfid record:  RFID code: {}. GroupID: {}. MusicOption {}".format(request.json["rfId"],
                                                                                              request.json["group_id"],
                                                                                              request.json[
                                                                                                  "musicOption_id"]))

    rfid = rfidDB.createRfidUser(request.json["rfId"], request.json["group_id"], request.json["musicOption_id"])
    return jsonify({'rfid': rfid}), 201


@app.route('/api/v1.0/contacts/<contactId>', methods=['GET'])
def get_contact(contactId):
    logger.debug("Retrieve contact {} from database.".format(contactId))
    contact = contactDB.get(contactId)
    return jsonify(contact), 200


@app.route('/api/v1.0/rfid/<rfidCode>', methods=['GET'])
def get_rfidEntry(rfidCode):
    logger.debug("Retrieve rfid Entry {} from database.".format(rfidCode))
    rfidEntry = rfidDB.getByRfid(rfidCode)
    return jsonify(rfidEntry), 200


@app.route('/api/v1.0/musicOptions/<rfidCode>', methods=['GET'])
def get_musicOptionByRfid(rfidCode):
    logger.debug("Retrieve rfid Entry {} from database.".format(rfidCode))
    rfidEntry = rfidDB.getByRfid(rfidCode)
    rfidGroup = rfidEntry["group_id"]
    if rfidGroup is not None and rfidGroup != "":
        message = "John Carnell is coming.  Hide"
        post_contact_by_group(rfidGroup, message)
    musicOption = musicOptionDB.getByMusicId(rfidEntry["musicOption_id"])
    return jsonify(musicOption), 200


@app.route("/api/v1.0/contacts", methods=['GET'])
def get_all_contacts():
    logger.debug("Retrieving al co94ntacts in the database")
    contacts = contactDB.getAll()
    return jsonify(contacts), 200


@app.route("/api/v1.0/groups", methods=['GET'])
def get_all_groups():
    logger.info("Retrieving all groups from the /api/v1.0/groups method")
    groups = groupDB.getAll()
    return jsonify(groups), 200


@app.route("/api/v1.0/musicOptions", methods=['GET'])
def get_all_musicOptions():
    logger.info("Retrieving all music options from the /api/v1.0/musicOptions method")
    musicOptions = musicOptionDB.getAllMusicOptions()
    return jsonify(musicOptions), 200

@app.route("/api/v1.0/musicOptions", methods=['POST'])
def create_musicOption():
    logger.debug("Creating a Music Option record: musicTitle: {}. fileName {}".format(request.json["musicTitle"],
                                                                                      request.json["fileName"]))
    musicOptionID = musicOptionDB.createMusicOptionEntry(request.json["musicTitle"], request.json["fileName"])
    return jsonify(musicOptionID), 200


@app.route('/api/v1.0/contacts/groups/<groupId>', methods=['GET'])
def get_contact_by_group(groupId):
    logger.debug("Retrieving all contacts belong to group {}.".format(groupId))
    contacts = contactDB.getAllByGroupId(groupId)
    return jsonify(contacts), 200


@app.route('/api/v1.0/contacts/groups/<groupId>/notify', methods=['POST'])
def post_contact_by_group(groupId):
    text = request.json["msgText"]
    return post_contact_by_group(groupId, text)


def post_contact_by_group(groupId, text):
    for contact in contactDB.getAllByGroupId(groupId):
        logger.info("Attempting to notify contact: {} {} with message {}".format(contact["firstName"],
                                                                                 contact["lastName"],
                                                                                 text))
        contact["msgText"] = text
        contactBody = json.dumps({"contacts": [contact]})

        http_obj = Http(".cache")
        (resp, content) = http_obj.request(uri="http://notifier:5010/api/v1.0/notify"
                                           , method='POST', body=contactBody,
                                           headers={'Content-type': 'application/json',
                                                    'tmx-correlation-id': str(utils.request_id())})

        time.sleep(.5)

        if (resp.status == 200):
            app.logger.info("Retrieved content back from: {}".format(content.decode("utf-8")))
        else:
            print("Error encountered when looking up contact data.  No data returned")

    return jsonify([]), 200

@app.route('/api/v1.0/contacts/seed', methods=['POST'])
def post_load_seed_data():
    logger.info("Loading the seed data into the database")
    loadSeedData()

    return jsonify([]), 200


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

    logger.info("Loading the third group of data.")
    groupId3 = groupDB.create("Schneider Trucking", "Edge Infrastructure Room")
    contactId = contactDB.create("John", "Carnell", "19202651560", groupId3)
    contactId = contactDB.create("Aidan", "Zimmermann", "19194411544", groupId3)
    contactId = contactDB.create("Sean", "Xiao", "19193608657", groupId3)
    contactId = contactDB.create("Brad", "Segiobiano", "19194279072", groupId3)

    logger.info("Loading the fourth group of data.")
    musicOption1 = musicOptionDB.createMusicOptionEntry("Whatta Man - Salt and Pepper", "Whataman.mp3")
    musicOption2 = musicOptionDB.createMusicOptionEntry("Crazy Train - Ozzy Osbourne", "Crazytrain.mp3")
    musicOption3 = musicOptionDB.createMusicOptionEntry("Imperial March - Star Wars", "Imperialmarch.mp3")
    musicOption4 = musicOptionDB.createMusicOptionEntry("Super Bon Bon - Sour Coughing", "Bonbon.mp3")
    musicOption5 = musicOptionDB.createMusicOptionEntry("Circle of Life - Lion King", "Circleoflife.mp3")
    musicOption6 = musicOptionDB.createMusicOptionEntry("Hang Up Your Hangups - Herbie Hancock", "Hangups.mp3")
    musicOption7 = musicOptionDB.createMusicOptionEntry("Stayin' Alive - Bee Gees", "Stayinalive.mp3")
    musicOption8 = musicOptionDB.createMusicOptionEntry("Shaft Theme Song - Issac Hayes", "ShaftA.mp3")
    musicOption9 = musicOptionDB.createMusicOptionEntry("Iron Man - Black Sabbath", "Ironman.mp3")
    musicOption10 = musicOptionDB.createMusicOptionEntry("Symphony No.5 - Beethoven", "Beethoven5.mp3")
    musicOption11 = musicOptionDB.createMusicOptionEntry("Earfquake - Tyler the Creator", "Earfquake.mp3")
    musicOption12 = musicOptionDB.createMusicOptionEntry("John Cena Theme Song", "Cenatheme.mp3")

    rfid = rfidDB.createRfidUser("11111111", groupId, musicOption1)
    rfid = rfidDB.createRfidUser("22222222", groupId2, musicOption2)
    rfid = rfidDB.createRfidUser("33333333", groupId3, musicOption3)
    rfid = rfidDB.createRfidUser("3099822457", "", musicOption4) #brent
    rfid = rfidDB.createRfidUser("3699974525", "", musicOption1) #john
    rfid = rfidDB.createRfidUser("3699974493", "", musicOption7) #lance
    rfid = rfidDB.createRfidUser("3699974461", "", musicOption2) #kal
    rfid = rfidDB.createRfidUser("3699976189", groupId3, musicOption5) #brad
    rfid = rfidDB.createRfidUser("3699976125", "", musicOption6)  #eric
    rfid = rfidDB.createRfidUser("3699936861", "", musicOption11)  #sean
    rfid = rfidDB.createRfidUser("3699687133", "", musicOption12)  #jake

    groupId4 = groupDB.create("Testing ", "Testing Group")
    rfid = rfidDB.createRfidUser("77777777", groupId4, musicOption1)
    contactId = contactDB.create("Lance", "Miller", "18044990969", groupId4)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
