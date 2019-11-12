from easygui import *
import sys
from gui_utils import *

while 1:
    introScreen()
    RFID = rfidScreen()
    song = songScreen()
    postSelection(RFID, song)
