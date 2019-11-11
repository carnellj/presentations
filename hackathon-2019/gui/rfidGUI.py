from easygui import *

msg = "Swipe your RFID"
title = "Register your RFID"
RFID = enterbox(msg,title)

# make sure that none of the fields was left blank
while 1:
    errmsg = ""
    if RFID == "":
        errmsg = "RFID may not be blank"
        RFID = enterbox(errmsg, title)
    if errmsg == "": break # no problems found

msg = "Choose your theme song"
title = "Choose Theme Song"
songChoices = ["a", "b", "c"]
song = choicebox(msg, title, songChoices)

# make sure that none of the fields was left blank
while 1:
    errmsg = ""
    if song == None:
        errmsg = "Please select a song"
        song = choicebox(errmsg, title, songChoices)
    if errmsg == "": break # no problems found

print(f"RFID was {RFID}. Song selected was {song}.")

#TODO: post RFID + song to service endpoint