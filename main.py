# package
import os
from dotenv import load_dotenv # env variable
from time import sleep as tsleep # time at the end
import curses # Terminal User Interface
from curses import wrapper # run Terminal User Interface
# myclass (assets/myclass)
from assets.myclass.slashCommand import SlashCommand # react to command
from assets.myclass.writeMessage import WriteMessage # write data on message pad
from assets.myclass.messageListener import MessageListener # react to incoming message
from assets.myclass.presenceListener import PresenceListener # react to incoming presence
# myfunc (assets/myfunc)
from assets.myfunc.editwin import feditwin # create a window to get message
from assets.myfunc.initPubNub import initPubNub # init PubNub object
from assets.myfunc.sanitizeStr import sanitizeStr # escape char in a message
from assets.myfunc.draw_rectangle import draw_rectangle # to fit window get message
from assets.myfunc.defineWindowArea import (defineWindowArea, # create localisation
                                            define_pad_loc) # of elements

# load env variable
load_dotenv(dotenv_path="assets/doc/data/.env")

def edit_writemessage_pad(pad_loc, writemessage):
    n_line, n_col, uly, ulx, lry, lrx = define_pad_loc(pad_loc)
    writemessage.update_loc(n_line, n_col, uly, ulx, lry, lrx)

def edit_stdscr_window(stdscr):
    stdscr.addstr(0, 0, "chat app [v0.1]")
    stdscr.refresh()

def main(stdscr):
    COLS = curses.COLS; LINES = curses.LINES # pylint: disable=no-member
    # define all localisation of elements
    pad_loc, rectangle_loc, editwin_loc = defineWindowArea(LINES, COLS)

    #### the recv message screen
    writemessage = WriteMessage()
    edit_writemessage_pad(pad_loc, writemessage)

    # PubNub object initialized in assets/myfunc/initPubNub;py
    o_pubnub = initPubNub(stdscr)

    edit_stdscr_window(stdscr) # header
    writemessage.write_start_up_message(f"{o_pubnub.uuid}") # welcome message
    # draw rectangle (from assets/myfunc/draw_rectangle.py)
    draw_rectangle(stdscr, rectangle_loc, "message :")
    
    # set message and presence listener
    o_pubnub.add_listener(MessageListener(writemessage))
    o_pubnub.add_listener(PresenceListener(writemessage))
    # subscribe to the main channel
    o_pubnub.subscribe().channels("general").with_presence().execute()
    o_pubnub._channel_name = "general" # we create a custom variable to keep 
    #a trace of the channel subscribed (if order to switch channel[not availible now])
    
    # SlashCommand object from assets/myclass/slashCommand.py
    commandSlash_handler = SlashCommand(writemessage, o_pubnub)
    
    #### the send message screen
    stay_connected = True
    while stay_connected:
        editwin, box = feditwin(editwin_loc)
        message = box.gather()
        message = sanitizeStr(message)
        if message.startswith('/'):
            stay_connected = commandSlash_handler.run_command(message)
        else:
            channel = o_pubnub._channel_name
            o_pubnub.publish().channel(channel).message(message).sync()
        editwin.erase()
        curses.update_lines_cols()
        # resize the window localisation if resize terminal detected (after send a message)
        if curses.LINES != LINES or curses.COLS != COLS: # pylint: disable=no-member
            LINES = curses.LINES; COLS = curses.COLS # pylint: disable=no-member
            pad_loc, rectangle_loc, editwin_loc = defineWindowArea(LINES, COLS)
            draw_rectangle(stdscr, rectangle_loc, "message :")
            edit_writemessage_pad(pad_loc, writemessage)
            edit_stdscr_window(stdscr)

wrapper(main)
tsleep(1)
print("good bye")
os._exit(1)