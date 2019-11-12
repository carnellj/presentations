from easygui import *
import urllib3
import sys
import json

http = urllib3.PoolManager()

def introScreen():
    msg = "Do you want to scan an RFID?"
    title = "Please Confirm"
    if ccbox(msg, title):     # show a Continue/Cancel dialog
        pass  # user chose Continue
    else:  # user chose Cancel
        sys.exit(0)

def rfidScreen():
    msg = "Swipe your RFID"
    title = "Register your RFID"
    RFID = enterbox(msg,title)

    # make sure that none of the fields was left blank
    while 1:
        errmsg = ""
        if RFID == "" or RFID == None:
            errmsg = "RFID may not be blank"
            RFID = enterbox(errmsg, title)
        if errmsg == "": break # no problems found
    
    return RFID

def songScreen():
    msg = "Choose your theme song"
    title = "Choose Theme Song"
    r = http.request('GET', 'http://localhost:5000/api/v1.0/musicOptions')
    songs = json.loads(r.data)
    songChoices = [x['musicTitle'] for x in songs]
    print(f'song choices {songChoices}')
    song = choicebox(msg, title, songChoices)

    # make sure that none of the fields was left blank
    while 1:
        errmsg = ""
        if song == None:
            errmsg = "Please select a song"
            song = choicebox(errmsg, title, songChoices)
        if errmsg == "": break # no problems found
    
    songId = [x['musicOption_id'] for x in songs if x['musicTitle'] == song][0]
    return songId

def postSelection(RFID, songId):
    data = {"rfId":RFID, "musicOption_id": songId, "group_id":""}
    encoded_data = json.dumps(data).encode('utf-8')
    r = http.request('POST', 'http://localhost:5000/api/v1.0/rfid', body=encoded_data, headers={'Content-Type': 'application/json'})
    return 1