#Gère le deck des catastrophes

import discord
from discord.ext import commands
import random
import math
import json
import re
import os
import subprocess
from Core.config import ArusuConfig
from Core.ErrorHandler import LogError, ErrorEmbed

class DeckCatastrophe() :
    def __init__(self) :
        self.CogName = "DeckCatastrophe"
        self.config = ArusuConfig()
            
        try :
            if self.config.DATA["Default_Deck"] != "default" : 
                with open(f"./Data/Custom/Deck/{self.config.DATA['Default_Deck']}.json", 'r', encoding='utf-8') as f :
                    self.CARDS = json.load(f)
            else : 
                with open("./Data/Default/Deck/DeckCatastrophe.json", 'r', encoding='utf-8') as f:
                    self.CARDS = json.load(f)
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="Init", Error=e)
            self.config.update(index='Default_Deck', value="default")
        
        self.items_per_page = 20
        self.pages = math.ceil(self.count() / self.items_per_page)
    
    # Embed for card effect / Card Drawn
    def create_card_embed(self, CardsList):  
        List = ""
        if len(CardsList) >= 1 and len(CardsList) <= 30 :
            for CardName in CardsList :
                List += f"**{CardName}** : \n {self.CARDS[CardName]} \n\n"

            embed = (discord.Embed(title="Deck des catastrophes",
                                description=List,
                                color = discord.Color.from_str(self.config.DATA["BOT_EMBED_COLOUR"])))
            
        if len(CardsList) > 30 and len(CardsList) <= 100 :
            for CardName in CardsList :
                List += f"**{CardName}**\n"

            embed = (discord.Embed(title="Deck des catastrophes",
                                description=List,
                                color = discord.Color.from_str(self.config.DATA["BOT_EMBED_COLOUR"])))
            
        if len(CardsList) > 100 : 
            embed = (discord.Embed(title="Deck des catastrophes",
                                description="Error : Too many cards",
                                color = discord.Color.from_str(self.config.DATA["BOT_EMBED_COLOUR"])))
        return embed

    #Embed for the card list
    def create_embed_list(self, page : int = 1):

        start = (page - 1) * self.items_per_page
        end = start + self.items_per_page

        try :
            List = ""
            CardTitle = []
            CardTitle = list(self.CARDS.keys()) #Pourquoi c'est pas une liste de base sérieusement
            try :
                for i, Card in enumerate(CardTitle[start:end], start=start):
                    List += f"**{Card}** : {self.CARDS[Card]} \n"
            except Exception as e :
                LogError(CogName=self.CogName, CogFunct="create_embed_list", Error=e)

            embed = (discord.Embed(title="Deck des catastrophes",
                                description=List,
                                color = discord.Color.from_str(self.config.DATA["BOT_EMBED_COLOUR"])).set_footer(text=f"Page {page}/{self.pages}"))
            return embed
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="create_embed_list", Error=e)
            
    def create_deck(self, Deck_Name) :
        try :
            New_Deck = {"Example Card" : "Example Effect"}
            try :
                subprocess.run([f"touch ./Data/Custom/Deck/{Deck_Name}.json"], check = True)
            except Exception as e:
                subprocess.run(["cd ./Data/Custom","mkdir Deck", "cd ../../"], check = True) #No such directory error
                subprocess.run([f"touch ./Data/Custom/Deck/{Deck_Name}.json"], check = True)
            with open(f"./Data/Custom/Deck/{Deck_Name}.json", 'w', encoding='utf-8') as outf :
                    json.dump(New_Deck, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
                    self.config.update(index='Default_Deck', value=f"{Deck_Name}") 
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="create_deck", Error = e)
    
    def list_decks(self) : 
        try :
            list = ""
            for root,dirs,files in os.walk("./Data/Custom/Deck"):
                files.sort()
                for filename in files :
                    list += f"{filename} \n"
            embed = discord.Embed(title="List of available decks", description=list, color = discord.Color.from_str(self.config.DATA["BOT_EMBED_COLOUR"]))
            return embed
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="list_decks", Error = e)
    
    def remove_deck(self, Deck_Name) : 
        try : 
            os.remove(f"./Data/Custom/Deck/{Deck_Name}.json")
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="remove_deck", Error = e)
            
    def change_main_deck(self, Deck_Name) : 
        try : 
            if Deck_Name != "default" : 
                with open(f"./Data/Custom/Deck/{Deck_Name}.json", 'r', encoding='utf-8') as f :
                    self.CARDS = json.load(f)
            else : 
                with open("./Data/Default/Deck/DeckCatastrophe.json", 'r', encoding='utf-8') as f:
                    self.CARDS = json.load(f)
        except Exception as e :
            LogError(self.CogName, "change_main_deck", e)
    
    def add_card(self, NAME, Effect) :
        try :
            self.CARDS[NAME] = Effect
            if self.config.DATA["Default_Deck"] != "default" : 
                with open(f"./Data/Custom/Deck/{self.config.DATA['Default_Deck']}.json", 'w', encoding='utf-8') as outf :
                    json.dump(self.CARDS, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)   
            else : 
                with open("./Data/Custom/Deck/CustomDeckCatastrophe.json", 'w', encoding='utf-8') as outf:
                    json.dump(self.CARDS, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
                    self.config.update(index='Default_Deck', value="CustomDeckCatastrophe")      
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="add_card", Error = e)

    def rm_card(self, NAME) :
        try :
            del self.CARDS[NAME]
            if self.config.DATA["Default_Deck"] != "default" : 
                with open(f"./Data/Custom/Deck/{self.config.DATA['Default_Deck']}.json", 'w', encoding='utf-8') as outf :
                    json.dump(self.CARDS, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)   
            else : 
                with open("./Data/Custom/Deck/CustomDeckCatastrophe.json", 'w', encoding='utf-8') as outf:
                    json.dump(self.CARDS, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
                    self.config.update(index='Default_Deck', value="CustomDeckCatastrophe")    
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="rm_card", Error = e)

    def list(self) : #J'ai pas de solution très élégante pour le moment en considérant la limite de charactère de discord
        try :
            embed_list = []
            for i in range(self.pages) :
                Emb = self.create_embed_list(page=i+1)
                embed_list.append(Emb)
            return embed_list
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="list", Error = e)

    def count(self) :
        return int(len(self.CARDS))

    def effect(self, Carte) :
        try :
            if Carte in self.CARDS : 
                CardEffect = str(Carte)+ " : " + str(self.CARDS[Carte])
                return CardEffect
            else :
                return "Invalid card name"
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="effect", Error = e)
            return "Could not send card effect"
        
    def draw(self, nb : int) :
        self.drawn = []
        if nb > 1000 :
            return
        for i in range (0, nb):
            carte = random.choice(tuple(self.CARDS.keys()))
            self.drawn.append(carte)
        return self.drawn
    

class Deck(commands.Cog):
    """
    Deck des catastrophes
    """

    def __init__(self, bot):
        self.bot = bot
        self.Deck = DeckCatastrophe()
        
    @commands.command(name = "deck", usage = "[nombre]", description = "Tire une carte du deck des catastrophes", aliases = ["dick"])
    async def drawmain(self, ctx, nb = 1):
        """
        Tire une carte du deck des catastrophes
        """
        await ctx.send(embed = self.Deck.create_card_embed(self.Deck.draw(int(nb))))
    
    @commands.command(name = "deck_effect", usage = '["Carte"]', description = "Donne l'effet d'une carte du deck. Le nom de la carte doit être entre guillemet.")
    async def effetmain(self, ctx, CardName):
        """
        Donne l'effet d'une carte du deck. Le nom de la carte doit être entre guillemet.
        """
        await ctx.send(self.Deck.effect(CardName))
    
    @commands.command(name = "deck_list", usage = "", description = "Liste l'intégralité des cartes du deck ainsi que leur effet.")
    async def listmain(self, ctx, page : int = 1):
        """
        Liste l'intégralité des cartes du deck ainsi que leur effet.
        """
        for element in self.Deck.list() :
            await ctx.send(embed = element)
        
    @commands.command(name = "deck_count", usage = "", description = "Donne le nombre de carte dans le deck")
    async def nombremain(self, ctx):
       """
       Donne le nombre de carte dans le deck
       """
       await ctx.send(self.Deck.count())

    @commands.group(name = "deck_set", invoque_without_command = True, aliases = ["dick_set"])
    @commands.has_permissions(administrator = True)
    async def deckmain(self, ctx): #Utilise le framework de base pour list les arguments
        """
        Commande maitre pour gérer le deck des catastrophes
        """
        pass    

    @deckmain.command(name = "add_card", usage = '["Card Name"] ["Card Effect"]', description = "Adds a card to the deck")
    async def add_card(self, ctx, CardName, CardEffect) :
        """
        Adds a card to the deck
        """
        try :
            self.Deck.add_card(NAME= CardName, Effect=CardEffect)
            await ctx.send(f"`{CardName} : {CardEffect}` has been added to the Deck.")
        except Exception as e:
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error while adding card to deck")

    @deckmain.command(name ="rm_card", usage = '["Card Name]', description = "Removes a card from the deck")
    async def rm_card(self, ctx, CardName) :
        """
        Removes a card from the deck
        """
        try :
            self.Deck.rm_card(NAME=CardName)
            await ctx.send(f"`{CardName}` has been removed from the deck.")
        except Exception as e:
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error while removing card from deck")
            
    @deckmain.command(name = "add_deck", usage = '["Deck_Name"]', description = "Creates a new deck")
    async def add_deck(self, ctx, Deck_Name) :
        """
        Creates a new deck
        """
        try :
            self.Deck.create_deck(Deck_Name)
            await ctx.send(f"{Deck_Name} has been created.")
        except Exception as e:
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error while creating deck")
    
    @deckmain.command(name = "rm_deck", usage = '["Deck_Name"]', description = "Removes a deck")
    async def rm_deck(self, ctx, Deck_Name) :
        """
        Removes a deck
        """
        try :
            self.Deck.remove_deck(Deck_Name)
            await ctx.send(f"{Deck_Name}` has been erased.")
        except Exception as e:
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error while erasing deck")
            
    @deckmain.command(name = "list_decks", usage = '', description = "Lists all decks")
    async def list_decks(self, ctx) :
        """
        Lists all decks
        """
        try :
            await ctx.send(embed = self.Deck.list_decks())
        except Exception as e:
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error listing decks")
            
    @deckmain.command(name = "change_deck", usage = '["Deck_Name"]', description = "Changes the main deck. 'default' to return to the default one")
    async def rm_deck(self, ctx, Deck_Name) :
        """
        Changes the main deck. 'default' to return to the default one
        """
        try :
            self.Deck.change_main_deck(Deck_Name)
            await ctx.send(f"{Deck_Name}` is now the main deck.")
        except Exception as e:
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error while chaning the main deck")
    
    ################################################################################################################################### 
    
    @commands.Cog.listener(name = "on_message")
    async def DeckSend(self, message):
        if message.author.id == self.bot.user.id:  #Stopping the bot from reading its own message
            return
        await message.channel.send(embed = self.Deck.create_card_embed(self.Deck.draw(int(re.findall(r"\btire *(\d+) *cartes?\b",message.content, flags=re.I)[0]))))
            
async def setup(bot : commands.Bot) :
    await bot.add_cog(Deck(bot))
