# package
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
from assets.myfunc.defineWindowArea import defineWindowArea # create localisaton of elements

# load env variable
load_dotenv(dotenv_path="assets/doc/data/.env")

def define_pad_loc(pad_loc):
    n_line = 100; n_col = pad_loc[3] - pad_loc[1] # n_line and n_col
    uly = pad_loc[0]; ulx = pad_loc[1] # uper-left y and x
    lry = pad_loc[2]; lrx = pad_loc[3] # lower-right y and x
    return n_line, n_col, uly, ulx, lry, lrx

def define_editwin_loc(editwin_loc):
    n_line = editwin_loc[2] - editwin_loc[0] or 1
    n_col = editwin_loc[3] - editwin_loc[1]
    y = editwin_loc[0]; x = editwin_loc[1]
    return n_line, n_col, y, x

def get_message_user(writemessage, o_pubnub, n_line, n_col, y, x):
    # SlashCommand object from assets/myclass/slashCommand.py
    commandSlash_handler = SlashCommand(writemessage, o_pubnub)
    stay_connected = True
    while stay_connected:
        editwin, box = feditwin(n_line, n_col, y, x)
        message = box.gather()
        message = sanitizeStr(message)
        if message.startswith('/'):
            stay_connected = commandSlash_handler.run_command(message)
        else:
            channel = o_pubnub._channel_name
            o_pubnub.publish().channel(channel).message(message).sync()
        editwin.erase()

def main(stdscr):
    # define all localisation of elements
    pad_loc, rectangle_loc, editwin_loc = defineWindowArea()

    #### the recv message screen
    n_line, n_col, uly, ulx, lry, lrx = define_pad_loc(pad_loc)
    writemessage = WriteMessage(n_line, n_col, uly, ulx, lry, lrx)

    # PubNub object initialized in assets/myfunc/initPubNub;py
    o_pubnub = initPubNub(stdscr)

    stdscr.addstr(0, 0, "chat app [v0.1]") # header
    writemessage.write_start_up_message(f"{o_pubnub.uuid}") # welcome message
    # draw rectangle (from assets/myfunc/draw_rectangle.py)
    draw_rectangle(stdscr, rectangle_loc, "message :")
    
    # set message and presence listener
    o_pubnub.add_listener(MessageListener(writemessage))
    o_pubnub.add_listener(PresenceListener(writemessage))
    # subscribe to the main channel
    o_pubnub.subscribe().channels("salut").with_presence().execute()
    o_pubnub._channel_name = "salut" # we create a custom variable to keep 
    #a trace of the channel subscribed
    
    #### the send message screen
    n_line, n_col, y, x = define_editwin_loc(editwin_loc) # 
    get_message_user(writemessage, o_pubnub, n_line, n_col, y, x)
    
    tsleep(1)
    o_pubnub.stop()

wrapper(main)
tsleep(1)