"""
file with only initPubNub function
"and set the debug level to CRITICAL"
"""
# get env
import os
# TUI for ask pseudo
import curses
from curses.textpad import Textbox, rectangle
# to ensure that every pseudo will be the only one
from random import randint
# PubNub
import pubnub
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.enums import PNReconnectionPolicy

pubnub.set_stream_logger('pubnub', level=pubnub.logging.CRITICAL)

def initPubNub(stdscr):
    """
    goal :
        ask for a pseudo if not in the path
    arg :
        stdscr : the screen initialised in main.py
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
            editwin = curses.newwin(1,min(16, curses.COLS-1),1,1) # pylint: disable=no-member
            editwin.keypad(True)
            box = Textbox(editwin)
            box.edit()
            pseudo = " ".join(box.gather().split())
        pseudo += "".join([str(randint(0,9)) for x in range(10)])
        with open("assets/document/data/.env", "a") as file:
            file.write(f"\nPSEUDO=\"{pseudo}\"")
        editwin.erase()

    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = os.getenv("SUB_KEY")
    pnconfig.publish_key = os.getenv("PUB_KEY")
    pnconfig.ssl = True
    pnconfig.cipher_key = os.getenv("CYPHER_KEY")
    pnconfig.uuid = pseudo
    pnconfig.reconnect_policy = PNReconnectionPolicy.EXPONENTIAL
    pnconfig.connect_timeout = 30

    return PubNub(pnconfig)