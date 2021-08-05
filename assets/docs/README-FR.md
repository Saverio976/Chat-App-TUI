# Chat App TUI

*pour voir la version anglaise de ce README, allez à /README.md*

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/aad0f93f865040beb83aaf1f5015e2bc)](https://www.codacy.com/gh/Saverio976/Chat-App-TUI/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Saverio976/Chat-App-TUI&amp;utm_campaign=Badge_Grade)

une app de tchat à but "personnel" réalisée pour m'améliorer en python

![chat-app-TUI](/assets/image/chat_app_tui.png "chat-app-TUI")

## téléchargement

1) dans un terminal/cmd
```shell
git clone https://github.com/Saverio976/Chat-App-TUI.git Chat-App-TUI-main
```

2) avec un navigateur internet

![downloadzip](/assets/document/img/downloadzip.png "downloadzip")

## mettre en place le projet

- ouvrez [un terminal / une invite de commande] dans le projet (tips pour Windows : assets/docs/open_cmd.md)

- et installez toutes les lib nécessaires

``shell
python -m pip install --upgrade pip
```

pour windows
```shell
python -m pip install -r aseets/requirements/win.txt
```

pour les autres os
```shell
python -m pip install -r assets/requirements/nix.txt
```

## lancer le projet

- dans un [terminal / une ligne de commande] ouverte dans le projet
```shell
python main.py
```

## mettre à jour le projet

- dans un [terminal / une ligne de commande] ouverte dans le projet
```shell
python settings/update.py
```

## Chat App

la première fois que vous allez la lancer, on va vous demander un pseudo

Ce pseudo sera afficher quand vous vous connecterez ou quand vous enverez un message, rejoindrez un salon, ...

# To Read
1)
vous pouvez maintenant envoyer un fichier et le telecharger (regardez /help pour plus de detail)

1)
une nouvelle commande qui arrive bientot ``/switch_channel <channel_name>`` mais pas encore terminée
vous devrez attendre encore un peu pour pouvoir parler dans plus d'un channel

2)
/set_cipher est de nouveau disponible ( une comande pour mettre un clefs de chiffrement)

3)
/history est une commande pour sauvegarder tous les messages dans un fichier ( assets/document/data/history.txt )
`/history True` : enregistrer les messages
`/history False` : arrete d'enregistrer les messages
par defaut à chaque début : False

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

## Merci à

[![first-beta-testor](https://img.shields.io/badge/First%20Beta%20Testor-Quentin-red)](https://instagram.com/chaque_64?igshid=p6k5bmwvknk)

[![second-beta-testor](https://img.shields.io/badge/Second%20Beta%20Testor-Luciolle24-blue)](https://github.com/luciolle24)

[![third-beta-testor](https://img.shields.io/badge/Second%20Beta%20Testor-DreamFail-green)](https://github.com/DreamFail)

## Contact

avant d'envoyer un mail, laissez une `issue` ou une `PR`

[![paradox-contact](https://img.shields.io/badge/Saverio-personnex976%40gmail.com-blue)](mailto:personnex976%40gmail.com)