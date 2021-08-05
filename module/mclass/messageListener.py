"""file with only MessageListener class"""

# PubNub related
from pubnub.callbacks import SubscribeCallback

class MessageListener(SubscribeCallback):
    def __init__(self, writemessage):
        """
        goal :
            listen all message send
        arg :
            writemessage : WriteMessage object (from assets/myclass/writeMessage.py)
        return :
            MessageListener class
        """
        self._writeMessage = writemessage

    def message(self, _, msg):
        content = msg.message
        author = f"{msg.publisher[:-10]}#{msg.publisher[-10:]}"

        if content == "/here":
            self._writeMessage.write_system_message(f"{author} est dans le channel")
            return None
        elif content == "[+inspect+]":
            self._writeMessage.write_signal_message(author, "FAIT SON INSPECTEUR")
            return None
        elif content.startswith("/ping "):
            self._writeMessage.write_ping_message(author, content[6:])
            return None
        else:
            self._writeMessage.write_new_message(author, content)
            return None
