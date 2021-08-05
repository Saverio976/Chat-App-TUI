"""
file with only initPubNub function
"and set the debug level to CRITICAL"
"""

# get env
import os
# random generator
import secrets, string
# TUI for ask pseudo
import curses
from curses.textpad import Textbox
# to ensure that every pseudo will be the only one

# PubNub
import pubnub
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.enums import PNReconnectionPolicy

pubnub.set_stream_logger('pubnub', level=pubnub.logging.CRITICAL)

def initPubNub(stdscr):
    """
    Ask for a pseudo if not in the path and init the pubnub.PubNub object.

    Parameters
    ----------
        stdscr: :class:curses._CursesWindow
            the screen initialised in main.py

    Returns
    -------
    :class:pubnub.PubNub
        with configuration
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
        alphabet = string.ascii_letters + string.digits
        pseudo += ''.join(secrets.choice(alphabet) for i in range(10))
        with open("assets/data/.env", "a") as file:
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