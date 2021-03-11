import curses

class SlashCommand:
    def __init__(self, writemessage, o_pubnub):
        self._writeMessage = writemessage
        self._o_pubnub = o_pubnub
        self._command = {
            "help" : ["help" ,self.help, "affiche les commandes disponibles + descriptions"],
            "fin" : ["fin", self.fin, "ferme la session et se deconnecte"],
            "here" : ["join", self.here, "envoi un message prévenant votre présence"],
            "set_cipher" : ["set_cipher <key>", self.set_cipher, "rajouter un chifrement gràce à cette clefs"],
            "ping" : ["ping <message>", self.ping, "envoi le message avec la couleur jaune"],
            "whohere" : ["whohere", self.whohere, "affiche les personnes présentes"]
        }

    def run_command(self, command, arg):
        trigger_command = self._command.get(command)[1]
        if trigger_command == None:
            return True
        return trigger_command(arg)

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
        self._o_pubnub.unsubscribe_all()
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
            set a cipher key to encrypt message and let other personn don't understand
        arg :
            arg : arg : the cypher key
        return 
            True # stay_connected will stay True
        """
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
                self._writeMessage.write_system_message(f"-> {member.uuid[:-10]}##{member.uuid[-10:]}")

        self._o_pubnub.here_now()\
            .channels("général")\
            .include_uuids(True)\
            .pn_async(here_now_callback)
        
        return True