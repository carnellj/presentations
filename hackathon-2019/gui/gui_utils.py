from easygui import *
from urllib import *
import sys

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
    #TODO: song choices to be retrieved via a GET request
    songChoices = ["a", "b", "c"]
    song = choicebox(msg, title, songChoices)

    # make sure that none of the fields was left blank
    while 1:
        errmsg = ""
        if song == None:
            errmsg = "Please select a song"
            song = choicebox(errmsg, title, songChoices)
        if errmsg == "": break # no problems found
    
    return song

def postSelection(RFID, song):
    print(f"RFID was {RFID}. Song selected was {song}.")
    return 1