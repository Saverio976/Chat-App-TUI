# Chat App TUI

*to see the french version of this README go to assets/docs/README-FR.md*

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/aad0f93f865040beb83aaf1f5015e2bc)](https://www.codacy.com/gh/Saverio976/Chat-App-TUI/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Saverio976/Chat-App-TUI&amp;utm_campaign=Badge_Grade)

a personal terminal chat app to improve my python skill

![chat-app-TUI](/assets/image/chat_app_tui.png "chat-app-TUI")

## download this chat app

1) on terminal/cmd
```shell
git clone https://github.com/Saverio976/Chat-App-TUI.git Chat-App-TUI-main
```

2) on a browser

![downloadzip](/assets/image/downloadzip.png "downloadzip")

## set up the project

- open a [terminal / command prompt] on this project path (tips for Windows : assets/docs/open_cmd.md)

- and install all required library
```shell
python -m pip install --upgrade pip
```

- on windows
```shell
python -m pip install -r aseets/requirements/win.txt
```

- on other os
```shell
python -m pip install -r assets/requirements/nix.txt
```

## launch the project

- on a [terminal / command prompt] open in the project directory
```shell
python main.py
```

## update the project

on the project path open a [terminal/ command prompt]
```shell
python settings/update.py
```

## Chat App

The first time you will run this app-like, it will ask you a pseudo

This pseudo will be print to all present people on a channel when you will send a message, join the channel, or other stuff

# To Read
1)
you can now send a file and download it (check /help for more info)

1)
a new incoming command named ``/switch_channel <channel_name>`` but not finish
so you need to wait more time to speak in more than one channel

2)
/set_cipher come back ! ( command to set a cipher key for sending message )

3)
/history is a command to save all message in a file (assets/data/history.txt)
`/history True` : save message
`/history False` : no longer save message
default on every launch : False

## in app commands : 
```
┌────────────────────────────────────────────────┬─────────────────────────────────────────────────────────┐
│ commande                                       │ expliquation                                            │
├────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ help                                           │ affiche toutes les commandes                            │
│ help <commande>                                │ affiche la description de cette commande                │
│ exit                                           │ ferme l'appli                                           │
│ whohere                                        │ affiche tous les membres connecté sur se salon          │
│ set_cipher                                     │ desactive les messages codé                             │
│ set_cipher <motClef>                           │ active les messages codé avec cette clefs de chifrement │
│ ping <message a envoyer >                      │ envoi un message en surbrilliance                       │
│ up                                             │ sroll vers le haut d'un message                         │
│ up <nombre>                                    │ scroll vers le haut du nombre de message                │
│ down                                           │ sroll vers le bas d'un message                          │
│ down <nombre>                                  │ scroll vers le bas du nombre de message                 │
│ history True                                   │ enregistre dans un fichier chaque message reçu          │
│ history False                                  │ desactive l'enregistrement                              │
│ send_file <chemin_absolu_du_fichier>           │ envoi un fichier dans le tchat                          │
│ download_file <ID du fichier> <nom du fichier> │ telecharge un fichier envoyé dans le tchat              │
└────────────────────────────────────────────────┴─────────────────────────────────────────────────────────┘
```

## Thanks

[![first-beta-testor](https://img.shields.io/badge/First%20Beta%20Testor-Quentin-red)](https://instagram.com/chaque_64?igshid=p6k5bmwvknk)

[![second-beta-testor](https://img.shields.io/badge/Second%20Beta%20Testor-Luciolle24-blue)](https://github.com/luciolle24)

[![third-beta-testor](https://img.shields.io/badge/Second%20Beta%20Testor-DreamFail-green)](https://github.com/DreamFail)

## Contact

before send a mail, please let an issue, or a PR

[![paradox-contact](https://img.shields.io/badge/Saverio-personnex976%40gmail.com-blue)](mailto:personnex976%40gmail.com)