# PubNub related
from pubnub.callbacks import SubscribeCallback

class MessageListener(SubscribeCallback):
    def __init__(self, writemessage):
        self._writeMessage = writemessage

    def message(self, o_pubnub, msg):
        #if o_pubnub.uuid == msg.publisher:
        #    return None

        content = msg.message
        author = f"{msg.publisher[:-10]}#{msg.publisher[-10:]}"

        if content == "/fin":
            self._writeMessage.write_system_message(f"{author} a quitté le channel")
            return None
        if content == "/here":
            self._writeMessage.write_system_message(f"{author} est dans le channel")
            return None
        if content.startswith("/ping "):
            self._writeMessage.write_ping_message(author, content[6:])
            return None

        self._writeMessage.write_new_message(author, content)
