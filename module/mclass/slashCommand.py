"""
file with only th SlashCommand class
"""

import curses
from module.function.sanitizeStr import sanitizeStr # pylint: disable=import-error

class SlashCommand:
    """
    goal :
        have all command in a simple class
    arg :
        writemessage : WriteMessage object (from assets/myclass/writeMessage.py)
        o_pubnub : PubNub object (init in assets/myfunc/initPubNub.py)
    return :
        a SlashCommand object
    """
    def __init__(self, writemessage, o_pubnub):
        self._writeMessage = writemessage
        self._o_pubnub = o_pubnub
        self._command = {
            "help" : ["help" ,self.help, "affiche les commandes disponibles + descriptions"],
            "fin" : ["fin", self.fin, "ferme la session et se deconnecte"],
            "here" : ["here", self.here, "envoi un message prévenant votre présence"],
            "set_cipher" : ["set_cipher [key]", self.set_cipher, "rajouter un chifrement gràce à cette clefs; si pas de clefs, enlève le chiffrement"],
            "ping" : ["ping [message]", self.ping, "envoi le message avec la couleur jaune"],
            "whohere" : ["whohere", self.whohere, "affiche les personnes présentes"],
            "up" : ["up [nb]", self.upPad, "aller vers le haut de nb ligne"],
            "down" : ["down [nb]", self.downPad, "aller vers le bas de nb ligne"],
            "history" : ["history <True/False>", self.set_historyfile_traceback, "Si True : met chaque message envoyé dans un fichier; si False : desactive"],
            #"switch_channel" : ["switch_channel <channel_name>", self.change_channel, "se connecte à un autre channel"],
            "send_file" : ["send_file <chemin_absolu>", self.send_file, "envoi un fichier pour que d'autres puissent l'avoir"],
            "download_file" : ["download_file <fileID> <fileNAME>", self.download_file, "télécharge un fichier en donnant son id et son nom"]
        }

    def run_command(self, message):
        """
        goal :
            the main entry for this class and run command
        arg :
            message : the message "send"
        return :
            True to stay connected
            False to disconnect
        """
        command = message.split()[0][1:] # we remove the "/"
        arg = " ".join(message.split()[1:]) # we remove the "/" + command
        if command not in self._command.keys():
            self._writeMessage.write_signal_message("cette commande n'existe pas")
            result = self.help(arg)
        else :
            func_command = self._command[command][1]
            result = func_command(arg)
        return result

    def help(self, arg):
        """
        goal :
            show all command availible
        arg :
            arg : arg
        return :
            True # stay_connected will stay True
        """
        msg1 = "Les éléments entre < > sont des informations indispensables"
        msg2 = "Les éléments entre [ ] sont des éléments optionels"
        msg3 = "Toutes les commandes commencent par un /"
        msg4 = "nom de la commande  ||  description"
        list_send = [msg1, msg2, msg3, msg4]
        for value in self._command.values():
            list_send.append(f"{value[0]} || {value[2]}")
        self._writeMessage._y = self._writeMessage._counter
        for x in list_send:
            self._writeMessage.write_system_message(x)
        return True

    def fin(self, _):
        """
        goal :
            disconnect from channels
        arg :
            _ : arg
        return :
            False # stay_connected will become False
        """
        channel = self._o_pubnub._channel_name
        self._o_pubnub.unsubscribe().channels(channel)
        self._writeMessage.write_system_message("Au revoir")
        return False

    def here(self, _):
        """
        goal :
            shwo a little message to say you are here
        arg :
            _ : arg
        return :
            True # stay_connected will stay True
        """
        self._o_pubnub.publish().channel("général").message("/here").sync()
        return True

    def set_cipher(self, arg):
        """
        goal :
            set a cipher key to encrypt message and let other don't understand
        arg :
            arg : arg : the cypher key
        return 
            True # stay_connected will stay True
        """
        if arg == "":
            self._o_pubnub.config.cipher_key = None
            self._writeMessage.write_system_message("cipher key deleted")
        else:
            self._o_pubnub.config.cipher_key = arg
            self._writeMessage.write_system_message("cipher key modified/created")
        return True
    
    def ping(self, arg):
        """
        goal :
            write arg in white on the channel
        arg :
            arg : arg : the message to send
        return :
            True # stay_connected will stay True
        """
        msg = "/ping " + arg
        self._o_pubnub.publish().channel("général").message(msg).sync()
        return True

    def whohere(self, _):
        """
        goal :
            show all present member
        arg :
            _ : arg
        return :
            True # stay_connected will stay True
        """
        def here_now_callback(result, status):
            if status.is_error():
                return True
            channel = result.channels[0]
            self._writeMessage.write_system_message("Liste des présents :")
            for member in channel.occupants:
                self._writeMessage.write_system_message(f"-> {member.uuid[:-10]}#{member.uuid[-10:]}")
        channel = self._o_pubnub._channel_name
        self._o_pubnub.here_now()\
            .channels(channel)\
            .include_uuids(True)\
            .pn_async(here_now_callback)
        msg = "[+inspect+]"
        self._o_pubnub.publish().channel(channel).message(msg).sync()
        return True

    def upPad(self, arg):
        """
        goal :
            scroll to the top of the message history
        arg :
            arg : nb line to go up [if no, = 1]
        return :
            True # stay_connected will stay True
        """
        if arg.isdigit():
            arg = int(arg)
        else:
            arg = 1
        self._writeMessage.PadUP(arg)
        return True

    def downPad(self, arg):
        """
        goal :
            scroll to the bottom of the message history
        arg :
            arg : nb line to go down [if no, = 1]
        return :
            True # stay_connected will stay True
        """
        if arg.isdigit():
            arg = int(arg)
        else:
            arg = 1
        self._writeMessage.PadDOWN(arg)
        return True

    def set_historyfile_traceback(self, arg):
        """
        goal :
            message send by user will be append to the assets/document/data/history.txt
            if arg is True
            if False : no file history traceback
        arg :
            arg : arg : True/False
        return :
            True # stay_connected will stay True
        """
        if arg not in ["True", "False"]:
            return self.help(arg)
        if arg == "True":
            self._writeMessage._is_history_file = True
            self._writeMessage.write_system_message("Traceback History File start !")
        else:
            self._writeMessage._is_history_file = False
            self._writeMessage.write_system_message("Traceback History File end !")
        return True

    def change_channel(self, arg):
        """
        goal :
            switch channel
        arg :
            arg : channel name
        return :
            True # stay_connected will stay True
        """
        if arg == "":
            return self.help(arg)
        channel = self._o_pubnub._channel_name
        self._o_pubnub.unsubscribe().channels(channel)
        self._o_pubnub.subscribe().channels(arg).with_presence().execute()
        self._o_pubnub._channel_name = arg
        self._writeMessage.write_system_message(f"switch to {arg} channel")
        return True

    def send_file(self, arg):
        """
        goal :
            send a file in the chat
        arg :
            arg : the path of the file
        return :
            True # stay_connected will stay True
        """
        if arg == "":
            return self.help(arg)
        try:
            fileobject = open(arg, 'rb')
        except:
            self._writeMessage.write_system_message("fichier introuvable")
            return True
        channel = self._o_pubnub._channel_name
        filename = arg.split("/")[-1]
        msg = {"filename" : filename}

        result = self._o_pubnub.send_file()\
                    .channel(channel)\
                    .file_name(filename)\
                    .message(msg)\
                    .should_store(False)\
                    .file_object(fileobject).sync()
        fileobject.close()
        msg = "pour telecharger le fichier envoye : /download_file "
        msg +=f"{sanitizeStr(result.result.file_id)} {sanitizeStr(result.result.name)}"
        self._o_pubnub.publish().channel(channel).message(msg).sync()
        return True

    def download_file(self, arg):
        """
        goal :
            download a file publish on a channel
        arg :
            arg :   first the fileID
                    seconde the fileNAME
        return :
            True # stay_connected will stay True
        """
        args = arg.split()
        if len(args) != 2:
            return self.help(arg)
        channel = self._o_pubnub._channel_name
        result = self._o_pubnub.download_file()\
                    .channel(channel)\
                    .file_id(args[0])\
                    .file_name(args[1]).sync()
        with open(args[1], "wb") as fd:
            fd.write(result.result.data)
        self._writeMessage.write_system_message("fichier téléchargé")
        return True