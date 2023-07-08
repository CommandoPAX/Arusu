#Gère le deck des catastrophes

from discord.ext import commands
import random
import json

class DeckCatastrophe() :
    def __init__(self) :
        with open(r"Cogs\DeckCatastrophe.json", 'r', encoding='utf-8') as f:
            self.CARDS = json.load(f)
    
    def add_card(self, NAME, Effect) :
        try :
            self.CARDS[NAME] = Effect
            with open(r"Cogs\DeckCatastrophe.json", 'w') as outf :
                    json.dump(self.CARDS, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
            
        except :
            print("Could not add card")

    def rm_card(self, NAME) :
        try :
            del self.CARDS[NAME]
            with open(r"Cogs\DeckCatastrophe.json", 'w') as outf :
                    json.dump(self.CARDS, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
        except :
            print("Could not remove card")

    def list(self) : #J'ai pas de solution très élégante pour le moment en considérant la limite de charactère de discord
        pass
    
    def count(self) :
        return int(len(self.CARDS))

    def effect(self, Carte) :
        try :
            if Carte in self.CARDS : 
                CardEffect = str(Carte)+ " : " + str(self.CARDS[Carte])
                return CardEffect
            else :
                return "Invalid card name"
        except :
            return "Could not send card effect"

class Deck(commands.Cog):
    """
    Deck des catastrophes
    """

    def __init__(self, bot):
        self.bot = bot
        self.Deck = DeckCatastrophe()
        
    @commands.command(name = "deck", usage = "[nombre]", description = "Tire une carte du deck des catastrophes", aliases = ["dick"])
    async def drawmain(self, ctx, nb = 1):
        """Tire une carte du deck des catastrophes"""
        for i in range (0, int(nb)):
              carte = random.choice(tuple(self.Deck.CARDS.keys()))
              Rep = "Vous avez tiré la carte : " + str(carte) + "\n" + str(self.Deck.CARDS[carte])
              await ctx.send(Rep)
    
    @commands.command(name = "deck_effect", usage = '["Carte"]', description = "Donne l'effet d'une carte du deck. Le nom de la carte doit être entre guillemet.")
    async def effetmain(self, ctx, CardName):
        """Donne l'effet d'une carte du deck. Le nom de la carte doit être entre guillemet."""
        await ctx.send(self.Deck.effect(CardName))
    
    @commands.command(name = "deck_list", usage = "", description = "Liste l'intégralité des cartes du deck ainsi que leur effet.")
    async def listmain(self, ctx):
        """Liste l'intégralité des cartes du deck ainsi que leur effet."""
        await ctx.send("Liste des effets du deck : \n") 
        Rep3 = ""
        for i, j in self.Deck.CARDS.items() :
            Rep3 = Rep3 + str(i) + " : " + str(j) + "\n"
            if len(Rep3) >= 1500 :
                await ctx.send(Rep3)
                Rep3 = ""
        await ctx.send(Rep3)
        
    @commands.command(name = "deck_count", usage = "", description = "Donne le nombre de carte dans le deck")
    async def nombremain(self, ctx):
       """Donne le nombre de carte dans le deck"""
       await ctx.send(self.Deck.count())

    @commands.group(name = "deck_set", invoque_without_command = True, aliases = ["dick_set"])
    @commands.is_owner()
    async def deckmain(self, ctx): #Utilise le framework de base pour list les arguments
        """
        Commande maitre pour gérer le deck des catastrophes
        """
        pass    

    @deckmain.command(name = "add", usage = '["Card Name"] ["Card Effect]', description = "Adds a card to the deck")
    async def add_cmd(self, ctx, CardName, CardEffect) :
        """
        Adds a card to the deck
        """
        try :
            self.Deck.add_card(NAME= CardName, Effect=CardEffect)
            await ctx.send(f"`{CardName} : {CardEffect}` has been added to the Deck.")
        except :
            await ctx.send("Could not add card to deck")

    @deckmain.command(name ="remove", usage = '["Card Name]', description = "Removes a card from the deck")
    async def rm_cmd(self, ctx, CardName) :
        """
        Removes a card from the deck
        """
        try :
            self.Deck.rm_card(NAME=CardName)
            await ctx.send(f"`{CardName}` has been removed from the deck.")
        except :
            await ctx.send(f"Could not remove `{CardName}` from the deck.")

async def setup(bot : commands.Bot) :
    await bot.add_cog(Deck(bot))
