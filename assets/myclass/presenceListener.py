"""
file with only PresenceListener class
"""
# PubNub related
from pubnub.callbacks import SubscribeCallback

class PresenceListener(SubscribeCallback):
    """
    goal :
        listen presence event
    arg :
        writemessage : WriteMessage object (from assets/myclass/writteMessage.py)
    return :
        PresenceListener object
    """
    def __init__(self, writemessage):
        self._writeMessage = writemessage

    def presence(self, o_pubnub, event):
        author = f"{event.uuid[:-10]}#{event.uuid[-10:]}"
        if event.event == "join":
            message = author + " vient d'arriver dans le channel"
            self._writeMessage.write_system_message(message)
        elif event.event == "leave":
            message = author + " vient de partir du channel"
            self._writeMessage.write_system_message(message)
        else:
            pass