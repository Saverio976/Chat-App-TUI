import os

from random import randint

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration

def initPubNub():
    """
    return :
        PubNub object with configuration
        and add MySubscribeCallBack listner
    """
    pseudo = os.getenv("PSEUDO")
    if pseudo == None:
        pseudo = input("Entrez un pseudo : ")
        pseudo += "".join([str(randint(0,9)) for x in range(10)])
        with open(".env", "a") as file:
            file.write(f"\nPSEUDO=\"{pseudo}\"\n")

    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = os.getenv("DEV_SUB_KEY")
    pnconfig.publish_key = os.getenv("DEV_PUB_KEY")
    pnconfig.ssl = True
    pnconfig.cipher_key = os.getenv("CYPHER_KEY")
    pnconfig.uuid = pseudo

    return PubNub(pnconfig)