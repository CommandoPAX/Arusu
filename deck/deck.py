from redbot.core import commands
import random

CarteDeck = {"Balance" : "Inverse votre alignement", "Comète" : "Oblitère un ennemi aléatoire durant le prochain combat", "Donjon" : "Cast Emprisonnement sur le pauvre fou ayant tiré la carte",
       "Général Puzzle" : "-1 à vos jets de save pour toujours", "Destin" : "Vous pouvez revenir dans le temps pour annuler un évenement", "Feu" : "Un ennemi puissant vous traque",
       "Idiot" : "-1 a tout vos attributs et vous retirez une carte", "Voyage astral à sans unique" : "Votre âme est envoyer dans le plan astral, aucun retour possible sans aide extérieur",
            "Soldat" : "Vous gagnez un lance-fusée capable d'invoquer vos alliés peu importe leur position", "Lune" : "Vous pouvez utiliser 1d4 wish",
            "Ruine" : "Vos 3 prochains jets de save ratent à coup sûr", "Mort" : "Vous mourrez", "Etoile" : "Vous choississez un de vos attributs, vous gagnez un +2",
            "Soleil" : "Full HP, et vous gagnez une arme de votre choix", "Terre" : "Tout vos objets perdent leur propriété spéciale",
            "Trône" : "+30 à votre prochain jet de diplomatie", "Vizier" : "Vous connaitrez la prochaine réponse à une unique question",
            "Vide" : "Vous êtes transporté dans une dimension/plan aléatoire", "Animal" : "Vous devenez un animal aléatoire",
            "Climatosceptique" : "Vous avez peur des arbres", "Nat 1" : "Vous tirez deux autres cartes", "Nat 20" : "Vous forcez quelqu'un à tirer deux cartes",
            "Gemme" : "Vous gagnez 100 000 golds", "Joker" : "+1 à tout vos attributs", "Voyage" : "Vous pouvez cast Téléportation",
            "Ombre" : "Fait spawn un double de vous-même que vous devez affronter et éliminer seul, si quelqu'un vous aide, une ombre de cette personne apparait",
            "Magicien" : "Vous accorde 4 sorts de niveau 5 ou - que vous choisissez, vous obtenez un spell slot par sort du même niveau que vous avez choisi.",
            "Roue" : "Vous ne pouvez plus vous déplacer qu'en faisant des saltos", "Loto" : "Vous pouvez reroll vos 3 prochains lancer de dés",
            "Expérience" : "Vous montez de niveau", "Hiérophante" : "Vous obtenez le livre sacrée de la religion vous convenant le plus",
            "Les Amoureux" : "Vous êtes liés à la personne la plus proche de vous. Vous ne pouvez plus vous éloignez à plus de 10m ou vous subissez 1d12 dégâts purs par tour.",
            "Le Monde" : "Tout le monde dans un rayon de 20m du tireur original tire une carte, y compris le tireur original",
            "Temps" : "Vous ne pouvez plus vieillir", "L'equilibre" : "Vos échecs et réussites critiques sont inversés.", "Ambivalent" : "Vous devez multiclass au niveau suivant",
            "Paladin" : "Choisissez un autre joueur, tout dégâts qu'il prend le passant à moins de 1PV vous sont transféré.",
            "Faiblesse" : "Les 5 prochaines attaques que vous subissez vous infligent 2 fois plus de dégâts",
            "Traitrise" : "Tirez des cartes jusqu'à en piocher 3 négatives. Vous infligez ces effets à un ou plusieurs alliés de votre choix",
            "Doppelganger" : "Vous gagnez un passif aléatoire d'une classe aléatoire même si celui-ci est inutile",
            "Explosion" : "Vous explosez, infligeant 6d6 dégâts à vous-même et aux créatures dans un rayon de moins de 6m",
            "Pigeon" : "Vous perdez toutes vos richesses", "Le soigneur" : "Vous gagnez 1d10 PV max", "Empereur" : "Vous pouvez cast domination une fois par jour",
            "Le politicien" : "Vous détectez tout les mensonges prononcé en votre présence", "La force" : "Vous réussisez tout les jets impliquant la force pendant 24h",
            "Hermite" : "Vous tombez inconscient", "Pendu" : "Vous perdez la moitié de vos PV", "Tempérance" : "Votre alignement devient Neutre Neutre",
            "Livre" : "+2 à votre attribut d'intelligence", "Aléatoire" : "Tout les effets des cartes que vous tirez sont transféré à une personne proche aléatoire",
            "Pentacle" : "Vous perdez tout votre équipement", "Dague" : "Vous perdez 1d4 PV", "Oubli" : "Tout le monde oublie votre existence jusqu'à l'instant présent",
            "Vision" : "Vous pouvez dorénavant voir à travers toutes les surfaces et illusions", "Baleine" : "Effet similaire à la carte mort mais c'est une baleine donc c'est pire",
            "Thanos" : "Un de vos alliés et un de vos ennemis meurt de facon permanente. Vous devez choisir qui meurt", "Conquête spatiale" : "Vous téléporte sur une planète aléatoire",
            "Trou noir" : "Invoque un trou noir sur votre position", "Ecureuil" : "Transforme d10 personnes à moins de 20m en écureuils pendant 1d3 heures",
            "Jouvence" : "Vous rajeunissez de 5d10+10 années pour un âge minimum de 3ans", "Stop" : "Vous ne pouvez plus entreprendre aucune action pendant 1d10 minutes",
            "Lag" : "Vous perdez vos deux prochains tours"}

class Deck(commands.Cog):
    """Deck des catastrophes"""

    def __init__(self, bot):
        self.bot = bot
    @commands.group(name = "deck", invoque_without_command = True)
    async def deckmain(self, ctx): #tire une carte tout le temps, commande à redef
        await ctx.send("Commande de base du deck des catastrophes. Arguments possibles : draw, effet, list, nombre.")
    
    @deckmain.command(name = "draw")
    async def drawmain(self, ctx)
        """Tire une carte du deck des catastrophes"""
        carte = random.choice(tuple(CarteDeck.keys()))
        Rep = "Vous avez tiré la carte : " + str(carte)
        await ctx.send(Rep)

    @deckmain.command(name = "effet")
    async def effetmain(self, ctx, Carte2):
        """Donne l'effet d'une carte du deck. Le nom de la carte doit être entre guillemet."""
        if Carte2 is in CarteDeck.keys() : 
            Rep = CarteDeck[Carte2]
            Rep2 = str(Carte2)+ " : " + str(Rep)
            await ctx.send(Rep2)
        else :
            await ctx.send("Le nom de la carte est invalide.")
    
    @deckmain.command(name = "list") #Ne marche pas, surement à cause de la limite de message de discord
    async def listmain(self, ctx):
        """Liste l'intégralité des cartes du deck ainsi que leur effet."""
        Rep3 = ""
        for i, j in CarteDeck.items() :
            Rep3 = Rep3 + str(i) + " : " + str(j) + "\n"
            if len(Rep3) >= 4000 :
                await ctx.send(Rep3)
                Rep 3 = ""
        await ctx.send(Rep3)
        
    @deckmain.command(name = "nombre")
    async def nombremain(self, ctx):
       """Donne le nombre de carte dans le deck"""
       n = int(len(CarteDeck))
       await ctx.send(n)
