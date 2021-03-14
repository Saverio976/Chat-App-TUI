# exit Sys, load Env
from sys import exit
from dotenv import load_dotenv
# time
from time import sleep as tsleep
# Terminal User Interface
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from assets.myclass.writeMessage import WriteMessage # Write data on pad
from assets.myfunc.defineWindowArea import defineWindowArea # return localisation
# Slash Command
from assets.myclass.slashCommand import SlashCommand # all command in a class
# PubNub related
from assets.myfunc.initPubNub import initPubNub # define the pubnub object
from assets.myclass.messageListener import MessageListener # listne message
from assets.myclass.presenceListener import PresenceListener # listne presence action
# sanitize string to publish
from assets.myfunc.sanitizeStr import sanitizeStr # escape \ and "

# load env variable
load_dotenv(dotenv_path="assets/doc/data/.env")

def main(stdscr):
    pad_localisation, rectangle_localisation, editwin_localisation = defineWindowArea()
    # read_messagae part of the screen
    n_line = 100
    n_col = pad_localisation[3] - pad_localisation[1]
    uly = pad_localisation[0]; ulx = pad_localisation[1]
    lry = pad_localisation[2]; lrx = pad_localisation[3]
    writemessage = WriteMessage(n_line, n_col, uly, ulx, lry, lrx)

    o_pubnub = initPubNub(stdscr)
    o_pubnub.add_listener(MessageListener(writemessage))
    o_pubnub.add_listener(PresenceListener(writemessage))
    o_pubnub.subscribe().channels("général").with_presence().execute()

    stdscr.addstr(0, 0, "chat app [v0.1]")
    stdscr.refresh()

    # send welcome start up message
    writemessage.write_start_up_message(f"{o_pubnub.uuid[:-10]}#{o_pubnub.uuid[-10:]}")

    commandSlash_handler = SlashCommand(writemessage, o_pubnub)

    # write_message part of the screen
    stdscr.addstr(rectangle_localisation[0]-1, rectangle_localisation[1], "message :")
    rectangle(stdscr, *rectangle_localisation) # pylint: disable=no-value-for-parameter
    stdscr.refresh()
    
    n_line = editwin_localisation[2] - editwin_localisation[0]
    n_col = editwin_localisation[3] - editwin_localisation[1]
    y = editwin_localisation[0]
    x = editwin_localisation[1]

    stay_connected = True
    while stay_connected:
        editwin = curses.newwin(n_line, n_col, y, x) # pylint: disable=no-value-for-parameter
        editwin.keypad(True)
        box = Textbox(editwin)
        box.edit()
        message = box.gather()
        message = " ".join(message.split())
        if message.startswith('/'):
            command = message.split()[0][1:] # we remove the "/"
            arg = " ".join(message.split()[1:]) # we remove the "/" + command
            stay_connected = commandSlash_handler.run_command(command, arg)
        else:
            message = sanitizeStr(message)
            o_pubnub.publish().channel("général").message(message).sync()
        editwin.erase()
    tsleep(1)
    o_pubnub.stop()
    tsleep(0.5)

wrapper(main)
exit()