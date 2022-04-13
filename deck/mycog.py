from redbot.core import commands
import random

deck = ["La **balance** vous fait face et votre manière de penser s'inverse", "Une **comète** tombe du ciel, annihilant tout sur son passage"
, "Un **donjon** vous emprisonne subitement", "Le **Général Puzzle** vous sourit, impossible de dire si c'est une bonne chose"
, "Connaissez votre **destin** pour mieux l'éviter", "Le **feu** éternel embrasera tout", "Qui est le plus **idiot** maintenant ?"
, "Une pile de **gemme** est toujours mieux qu'une pille de gemme pas", "J'ai plus d'idée donc je vais utiliser mon **joker**", "Vous avez gagné un bon pour un **voyage astral à sens unique**"
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

liste = "Règles : joueur doit annoncer combien de cartes il tire avant de le faire, les cartes seront tiré dans tout les cas même si la personne est incapacité.\n Balance : inverse votre alignement"

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
        await ctx.send(liste)
