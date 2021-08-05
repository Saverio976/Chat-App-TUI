"""File with only PresenceListener class."""

# PubNub related
from pubnub.callbacks import SubscribeCallback

class PresenceListener(SubscribeCallback):
    def __init__(self, writemessage):
        """
        Listen presence event

        Parameters
        ----------
        writemessage: :class:WriteMessage
            (from module/mclass/writteMessage.py)

        Returns
        -------
        :class:PresenceListener
        """
        self._writeMessage = writemessage

    def presence(self, _, event):
        author = f"{event.uuid[:-10]}#{event.uuid[-10:]}"
        if event.event == "join":
            message = author + " vient d'arriver dans le channel"
            self._writeMessage.write_system_message(message)
        elif event.event == "leave":
            message = author + " vient de partir du channel"
            self._writeMessage.write_system_message(message)
        else:
            pass