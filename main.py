### package
import os
import requests                                                             # check if you are connected to internet
import curses                                                               # Terminal User Interface
from curses import wrapper                                                  # run Terminal User Interface
from dotenv import load_dotenv                                              # env variable
from time import sleep as tsleep                                            # sleep at the end of the runing process
### class (module/mclass)
from module.mclass.slashCommand import SlashCommand                         # react to slash command
from module.mclass.writeMessage import WriteMessage                         # write data on message's pad
from module.mclass.messageListener import MessageListener                   # react to incoming message from pubnub
from module.mclass.presenceListener import PresenceListener                 # react to incoming presence from pubnub
### function (module/function)
from module.function.editwin import feditwin                                # create a window box to get message
from module.function.initPubNub import initPubNub                           # init pubnub.PubNub object
from module.function.sanitizeStr import sanitizeStr                         # escape 'escape char' in a message
from module.function.draw_rectangle import draw_rectangle                   # to fit window get message
from module.function.defineWindowArea import (
    defineWindowArea,                                                       # create localisation
    define_pad_loc                                                          # of elements
)

load_dotenv(dotenv_path="assets/data/.env")                                 # load env variable

is_connected = False
timer = 0
while not is_connected:
    tsleep(int(timer))
    try:
        requests.get('https://google.com')
    except requests.exceptions.ConnectionError:
        timer = timer * 1.2 + 1
        print(f"retrying in {int(timer)} second(s)")
    else:
        is_connected = True

def edit_writemessage_pad(pad_loc, writemessage):                           # update pad localisation (if the terminal change its size)
    n_line, n_col, uly, ulx, lry, lrx = define_pad_loc(pad_loc)
    writemessage.update_loc(n_line, n_col, uly, ulx, lry, lrx)

def edit_stdscr_window(stdscr):                                             # update the header message
    stdscr.addstr(0, 0, f"chat app [v{os.environ['VERSION']}]")
    stdscr.refresh()

def main(stdscr):
    COLS, LINES = curses.COLS, curses.LINES

    pad_loc, rectangle_loc, editwin_loc = defineWindowArea(LINES, COLS)     # define all localisation of elements

    #### the recv message screen
    writemessage = WriteMessage()
    edit_writemessage_pad(pad_loc, writemessage)

    o_pubnub = initPubNub(stdscr)                                           # PubNub object initialized in assets/myfunc/initPubNub.py

    edit_stdscr_window(stdscr)                                              # header
    writemessage.write_start_up_message(f"{o_pubnub.uuid}")                 # welcome message
    draw_rectangle(stdscr, rectangle_loc, "message :")                      # draw rectangle (from assets/myfunc/draw_rectangle.py)

    o_pubnub.add_listener(MessageListener(writemessage))                    # set message listener
    o_pubnub.add_listener(PresenceListener(writemessage))                   # set presence listener

    o_pubnub.subscribe().channels("general").with_presence().execute()      # subscribe to the main channel
    o_pubnub._channel_name = "general"                                      # we create a custom variable to keep
                                                                            #a trace of the channel subscribed
                                                                            # (in order to switch channel[not availible now])
    
    #### the send message screen
    commandSlash_handler = SlashCommand(writemessage, o_pubnub)             # SlashCommand object from assets/myclass/slashCommand.py

    stay_connected = True
    while stay_connected:
        editwin, box = feditwin(editwin_loc)
        message = box.gather()
        message = sanitizeStr(message)
        if message == '':                                                   # empty message -> dont send it
            pass
        elif message.startswith('/'):
            stay_connected = commandSlash_handler.run_command(message)
        else:
            channel = o_pubnub._channel_name
            o_pubnub.publish().channel(channel).message(message).sync()
        editwin.erase()
        curses.update_lines_cols()

        if curses.LINES != LINES or curses.COLS != COLS:                    # resize the window localisation if size of the terminal is modified (after send a message)
            LINES, COLS = curses.LINES, curses.COLS
            pad_loc, rectangle_loc, editwin_loc = defineWindowArea(LINES, COLS)
            draw_rectangle(stdscr, rectangle_loc, "message :")
            edit_writemessage_pad(pad_loc, writemessage)
            edit_stdscr_window(stdscr)

wrapper(main)
tsleep(1)
print("good bye")
os._exit(0)