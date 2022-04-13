from redbot.core import commands
import random

deck = ["La **balance** vous fait face et votre manière de penser s'inverse", "Une **comète** tombe du ciel, annihilant tout sur son passage"
, "Un **donjon** vous emprisonne subitement", "Le **Général Puzzle** vous sourit, impossible de dire si c'est une bonne chose"
, "Connaissez votre **destin** pour mieux l'éviter", "Le **feu** éternel embrasera tout", "Qui est le plus **idiot** maintenant ?"
, "Une pile de **gemme** est toujours mieux qu'une pile de gemme pas", "J'ai plus d'idée donc je vais utiliser mon **joker**", "Vous avez gagné un bon pour un **voyage astral à sens unique**"
, "Vos **soldats** seront toujours avec vous", "Je souhaite que la **lune** explose", "Les pouvoirs de la **ruine** sont capricieux", "La **mort** vous sourit",
 "Oh une **étoile** filante, faites un voeu !", "Le **soleil** vous irradie de ses UV bénéfiques", "Avec le temps, tout retournera à la **terre**"
 , "Pour ces exploits, un **trône** doit bien vous attendre quelque part", "Je sais toujours pas ce qu'est un **vizier**", "Le Saviez-vous ? Le **vide** n'est pas vide"
 , "Au fond, est tous des **animaux**", "Au secours un arbre m'attaque ! Michel, **climatosceptique** depuis 30 secondes.", "Que les Dieux des **dés** soient avec vous"
 , "Il est l'heure de partir en **voyage**", 'Surtout ne dites jamais "Tu n' "'" 'pas moi à votre **ombre**', "Respec **magicien** let's go", "La **roue**tourne va tourner"
 , "C'est comme jouer au **loto** mais en mieux", "Si seulement je pouvais avoir autant d'**experience**", "Je sais pas non plus ce qu'est un **hierophante**"
 , "**Les amoureux** sont pas très utile mais j'aime bien la métaphore", "A terme, tout le **monde** tirera une carte", "Le **temps** n'a plus cours en ces lieux"
 , "Tu dois rétablir l'**équilibre** dans les jets de dés !", "Dualité c'est cool, **ambivalence** c'est mieux", "En vrai, c'est pas vous la **sangsue**"
 , "Votre **faiblesse** vous trahira prochainement", "Quelle magnifique **traitrise**", "En tant que **grande prêtresse**, je peux passer un appel au MJ ?", 
 "C'est pas vraiment un **doppelganger** mais ca passe", "**Explosion** !", "Fallait pas acheter des jeux nintendo sale **pigeon**", "L'âge des **glace** va débuter. Vous préférez le chocolat ou la vanille ?"
 , "Vous avez la bénédiction de l'**impératrice**", "Pour l'**Empereur** !", "Votre volonté est actuellement dans un **chariot**", "Quelle **force** !"
 , "Redevenez l'**hermite** que vous avez toujours voulu être", "Le **pendu** vous promet de grandes richesses si vous prenez sa place", "La **tempérance**, c'est cool"
 , "C'est un peu comme passer un pacte avec le **diable**", "Le **Jugement** de STREAM;GATE France est impartial", "Aucun rapport avec une **épée**"
 , "Encore plus d'**aléatoire**", "Le **pentacle** satanique de la nudité", "Un bon coup de **dague** dans le dos, ca aide à se lever le matin", "Vous sombrez dans l'**oubli**"
 , "Rien n'échappe à votre **vision**", "Le **Chaos** se répend", "Pas encore la **baleine** !", "Votre **agilité** n'a d'égare que la grâce d'une tortue"
 , "Get **Thanos**'d", "La gloire du **LSMB** est éternelle", "C'est un **trou noir**, bonne chance", "Qui aurait cru que devenir un **écureuil** pourrait être si problématique ?"
 , "La Fontaine de **Jouvence** vous rajeunit", "Là c'est **stop**"]

liste1 = "Règles : joueur doit annoncer combien de cartes il tire avant de le faire, les cartes seront tiré dans tout les cas même si la personne est incapacité.\n Balance : inverse votre alignement\n Comète : oblitère un ennemi aléatoire durant le prochain combat\n Donjon : cast Emprisonnement sur celui qui a tiré la carte\n Général Puzzle : -1 à tout les jets de save pour toujours\n Destin : évite une situation au choix\n Feu : vous venez de vous faire un ennemi très puissant\n Idiot : -1 à toutes les stats et vous devez retirer une carte\n Gemme : gagne 100 000 valkyryen \n Joker : +1 à toutes les stats\n Voyage astral à sens unique : le corps fonctionne mais l'âme est ailleurs\n Soldat : vous gagnez un lance-fusée permettant d'invoquer de puissant allié\n Lune : donne accès à 1d2 Wish\n Ruine : 3 prochains jet de save ratent forcément\n Mort : passe à PV = -10 PV max\n Etoile : +2 à une stat de manière permanente\n Soleil : full PV + une arme puissante\n Terre : tout les items infusé ou puissant en votre possession disparaissent\n Trône : +6 au prochain jet de diplomatie\n Vizier : connait la réponse au prochain dilemme\n Vide : vous êtes transporté dans une dimension aléatoire\n Animal : vous transforme en un animal random de manière permanente\n Climatosceptique : vous gagnez une phobie sévère et incontrôlé des arbres\n Dés :  vous tirez deux cartes supplémentaires \n Voyage : vous téléportez instantanément dans une zone aléatoire situé à ~5km\n Ombre : fait spawn un double de vous-même que vous devez affronter et éliminer seul, si quelqu'un vous aide, une ombre de cette personne apparait"
liste2 = " Magicien : vous accorde 4 sorts de gigalomania de niveau 5 ou - que vous choisissez, vous obtenez un spell slot par sort du même niveau que vous avez choisi.\n Roue : une carte aléatoire du deck est détruite a jamais. Vous pouvez choisir de diminuer un de vos attributs de moitié pour sauver la carte.\n Loto : vous pouvez reroll vos 3 prochains lancer de dés.\n Expérience : vous montez de niveau\n Hiérophante : vous obtenez le livre sacré de la religion vous convenant le plus\n Les Amoureux : vous obtenez deux aimants capable de déplacer chacun 5kg jusqu'à une distance de 10m\n Monde : tout le monde dans un rayon de 10m autour du tireur original tire une carte.\n Temps : cast Arrêt temporel sur vous même\n Equilibre : les échecs critiques et réussites critiques sont inversés de manière permanente \n Ambivalent : votre prochain niveau doit être dépensé dans une autre classe que votre actuel\n Sangsue : choisissez un autre joueur, tout dégâts qu'il prend le passant à moins de 1PV vous sont transféré.\n Faiblesse : les 5 prochaines attaques que vous subissez vous infligent 2 fois plus de dégâts\n Traitrise : vous infligez 3 effets négatifs du deck à l'un de vos alliés\n Grande Prêtresse : vous pouvez poser une seul question au MJ qui doit répondre avec uniquement la vérité.\n Doppelganger : vous gagnez un passif d'une classe aléatoire \n Explosion : vous castez boule de feu au niveau 6 sur vous-même.\n Pigeon : vous perdez tout votre argent\n Glace : vous gagnez un puissant allié\n Impératrice : vous gagnez 1d10 PV max\n Empereur : vous pouvez cast domination une seule fois"
liste3 = " Chariot : +2 au vol-save de manière permanente\n Force : vous réussissez tout les jets impliquant la force pendant un jour\n Hermite : vous tombez inconscient\n Pendu : vous sacrifiez la moitié de vos PV max de manière permanente pour offrir un effet positif (hors la lune) à un allié\n Tempérance : change l'alignement pour neutre neutre\n Diable : vous infligez un effet négatif du deck à l'un de vos allié en échange d'un objet puissant\n Jugement : vous signez un contrat avec la personne la plus proche stipulant que vous sacrifierez votre vie pour elle. Si elle meurt avant vous, vous subissez l'effet Mort.\n Epée : +2 à votre stat d'intelligence\n Aléatoire : vous tirez un effet de la wild magic table\n Pentacle : vous perdez tout vos vêtements ainsi que votre armure\n Dague : vous perdez 1d4 PV\n Oubli : tout le monde oublie votre existence jusqu'à l'instant présent\n Vision : vous gagnez les effets de vraie vision de manière permanente \n Chaos : choisi 1d20 objet visible, ils tombent tous en panne de manière plus ou moins catastrophiques\n Baleine : une baleine vous tombe dessus (inévitable, et mort instantanée)\n Agilité : vous gagnez les effets de Liberté de mouvement de manière permanente\n Thanos : un de vos alliée ainsi que l'un de vos ennemis meurt. Vous pouvez choisir qui meurt.\n LSMB : vous téléporte sur une planète aléatoire.\n Trou noir : invoque un trou noir\n Ecureuil : transforme d10 personnes à moins de 20m en écureuils pendant 1d3 heures\n Jouvence : vous rajeunissez de 5d10+10 années pour un âge minimum de 3ans\n Stop : vous ne pouvez plus entreprendre aucune action pendant 1d10 minutes (excepté les actions vitales comme respirer)"

class Deck(commands.Cog):
    """Deck des catastrophes"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def deck(self, ctx):
        """Tire une carte du deck des catastrophes"""
        await ctx.send(random.choice(deck))

    @commands.command()
    async def decklist(self, ctx):
        """Liste les effets du deck des catastrophes"""
        await ctx.send(liste1)
        await ctx.send(liste2)
        await ctx.send(liste3)
