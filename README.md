# Arusu
Arusu est le bot officiel de STREAM;GATE France géré par votre humble serviteur.
Si vous avez des requêtes de plugin, vous pouvez me les envoyer.

## Installation

Installer l'Arusu Bot est assez simple, il vous suffit de :
1. Installer python 3.10.6
2. Download l'intégralité du repo
`git clone https://github.com/CommandoPAX/Arusu`
3. Installer les requirements
`pip install -r requirements.txt`
4. Installer FFMPEG
`sudo apt install ffmpeg`
5. Générer un Token sur le [portail developpeur](https://discord.com/developers/docs/intro) et le mettre dans "config.json"
6. Executer le fichier "main.py"

## Liste actuel des plugins :

### Bot status

- status [statut] [activity] [additionnal text]: change le statut du bot

### Music

- join : rejoint le salon vocal de l'auteur
- leave : quitte le salon vocal actuel
- now : affiche la musique jouée actuellement
- pause : met la  musique en pause
- play [search] : joue la musique via un URL ou une recherche
- queue [page] : affiche la queue
- remove [index] : enlève une musique de la queue
- resume : enlève la pause
- shuffle : met la queue en aléatoire
- skip : passe à la musique suivante
- stop : arrête la musique en cours et clear la queue
- summon [channel] : rejoint le salon vocal spécifié
- volume [volume] : change le volume

### Roll

- roll [xdy +z] : roll les dés spécifiés avec modificateurs

### Utils

- config_test : renvoie un test pour la config
- embed_colour [colour] : change la couleur de tout les embeds, prend un code hexadecimal comme argument
- ping : renvoie pong
- prefix : change le prefix du bot, requiert un redémarrage
- restart : redémarre le bot
- showsettings : renvoie toute la config sauf le token
- shutdown : éteins le bot

### Feur

- feur : permet d'activer / désactiver le plugin

### Deck

- deck [nombre] : tire le nombre spécifié de carte
- deck_count : renvoie le nombre de cartes dans le deck
- deck_effect [Nom de la carte] : renvoie l'effet de la carte
- deck_list : renvoie une liste de toutes les cartes du deck ainsi que leur effet
- deck_set : permet d'ajouter / supprimer des cartes

### Welcome

- leave_test : renvoie un message de départ
- leavemsg [message] : set le message de départ. {Member} pour spécifier le membre et {Server} pour le serveur
- leaveset [ID du salon] : set le salon pour le message de départ
- welcome_test : renvoie un message de bienvenue
- welcomemsg [message] : set le message de bienvenue. {Member} pour spécifier le membre et {Server} pour le serveur
- welcomeset [ID du salon] : set le salon pour le message de bienvenue

### Core

- help [Command or Cog (optionnal)] : renvoie l'aide du bot

## T.B.A.

- Alias (dynamique, une manière non dynamique existe déjà)
- Playlist
- Chatbot
