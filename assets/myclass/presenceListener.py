# PubNub related
from pubnub.callbacks import SubscribeCallback

class PresenceListener(SubscribeCallback):
    def __init__(self, writemessage):
        self._writeMessage = writemessage

    def presence(self, o_pubnub, event):
        if event.event == "join":
            message = f"{event.uuid[:-10]}#{event.uuid[-10:]} vient d'arriver dans le channel"
            self._writeMessage.write_system_message(message)
        if event.event == "leave":
            message = f"{event.uuid[:-10]}#{event.uuid[-10:]} vient de partir du channel"
            self._writeMessage.write_system_message(message)