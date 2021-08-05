"""File with only MessageListener class."""

# PubNub related
from pubnub.callbacks import SubscribeCallback

class MessageListener(SubscribeCallback):
    def __init__(self, writemessage):
        """
        Listen all message send.

        Parameters
        ----------
        writemessage: :class:WriteMessage
            (from module/mclass/writeMessage.py)

        Returns
        -------
        :class:MessageListener
        """
        self._writeMessage = writemessage

    def message(self, _, msg):
        content = msg.message
        author = f"{msg.publisher[:-10]}#{msg.publisher[-10:]}"

        if content == "[+inspect+]":
            self._writeMessage.write_signal_message(author, "FAIT SON INSPECTEUR")
            return None
        elif content.startswith("/ping "):
            self._writeMessage.write_ping_message(author, content[6:])
            return None
        else:
            self._writeMessage.write_new_message(author, content)
            return None
