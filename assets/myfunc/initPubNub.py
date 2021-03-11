# get env
import os

# TUI for ask pseudo
import curses
from curses.textpad import Textbox, rectangle

# to ensure that every pseudo will be the only one
from random import randint

# PubNub
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration

def initPubNub(stdscr):
    """
    return :
        PubNub object with configuration
        and add MySubscribeCallBack listner
    """
    pseudo = os.getenv("PSEUDO")
    if pseudo == None:
        pseudo = ""
        while len(pseudo) < 2:
            stdscr.addstr(0,0, "pseudo :")
            stdscr.refresh()
            editwin = curses.newwin(1,min(10, curses.COLS-1),1,1) # pylint: disable=no-member
            editwin.keypad(True)
            box = Textbox(editwin)
            box.edit()
            pseudo = " ".join(box.gather().split())
        pseudo += "".join([str(randint(0,9)) for x in range(10)])
        with open(".env", "a") as file:
            file.write(f"\nPSEUDO=\"{pseudo}\"")
        editwin.erase()

    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = os.getenv("DEV_SUB_KEY")
    pnconfig.publish_key = os.getenv("DEV_PUB_KEY")
    pnconfig.ssl = True
    pnconfig.cipher_key = os.getenv("CYPHER_KEY")
    pnconfig.uuid = pseudo

    return PubNub(pnconfig)