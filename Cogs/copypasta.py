#Plugin qui permet au bot d'envoyer une copypasta aléatoirement après un message

from discord.ext import commands
from config import ArusuConfig
from Core.ErrorHandler import LogError, ErrorEmbed
import random

class CopyPasta(commands.Cog):
    """Je ne suis pas désolé"""
    
    def __init__(self, bot):
        self.bot = bot
        self.CogName = "CopyPasta"
        self.config = ArusuConfig()
        self.answers = ["""Au fait, tu as déjà joué Final Fantasy XIV, le MMORPG critiquement acclamé avec un essai gratuit sans limite de temps te permettant d'aller jusqu'au niveau 60, et qui inclut la première expansion, Heavensward, qui a gagné de multiples awards ?""", "Oui mais non",
                        "UwU", ":3", "Tu veux tirer une carte ?", """Je vais au centre de depistage de mst uniquement pour la satisfaction de savoir que le personnel d'accueil pense que je baise. 
Je prend rendez-vous chaque mois, et ce jour est encore arrivé aujourd'hui. J'y serais dès demain à l'aube. En rentrant, je suis à la limite de l'orgasme lorsque l'infirmière de service me dit bonjour en m'appelant directement par mon prénom. 
Elle sait que je suis un habitué, que je baise, que ça ne s'arrête plus. Je sais pertinemment que les résultats reviendront à jamais négatifs, je suis bâtonnier après tout.
Je tiens un carnet du nombre de personnes qui m'ont vu faire un test et qui doivent forcément se dire que je suis actif. 
Depuis 2012, j'en suis à 264 personnes. Pouvez-vous en dire autant? Pouvez vous vous vanter que 264 personnes pensent que vous êtes un putain de défourailleur, de défiotteur?
J'attends votre réponse bande de sous-merdes. Vous remercierez Smaxy...""", """Je crois que les filles m'aiment bien parceque je suis un peu mystérieux comme Light Yagami, je suis toujours tout seul,
aux récrées je m'assoie sur un banc avec ma capuche et la tête baissé et quand quelque passe à coté de moi je chuchote des truc genre okamari no suzoki, ça ne veut rien dire mais ça fait mystique,
les gens sont intrigués."""]
        
    @commands.group(name = "pasta", description = "Main command to enable or disable the CopyPasta Cog")
    @commands.is_owner()
    async def pastamain(self, ctx) :
        """
        Main command to enable or disable the Feur Cog
        """
        pass
    
    @pastamain.command(name = "enable", usage = "", description = "Enables the cog")
    async def enable(self, ctx):
        """
        Enables the cog
        """
        try :
            self.config.update(f"{ctx.guild.id}.PastaEnabled", True)
            await ctx.send("Pasta enabled")
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="enable", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error enabling the cog")
    
    @pastamain.command(name = "disable", usage = "", description = "Disables the cog")
    async def disable(self, ctx):
        """
        Disables the cog
        """
        try :
            self.config.update(f"{ctx.guild.id}.PastaEnabled", False)
            await ctx.send("Pasta disabled")
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="disable", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error disabling the cog")

    ################################################################################################################################### 
    
    @commands.Cog.listener(name = "on_message")
    async def PastaAnswer(self, message):
        try :
            if self.config.DATA[f"{message.guild.id}.PastaEnabled"] != True : 
                return
            n = random.randint(1,200)
            if n != 1 :
                return
            AnswerMsg = random.choice((tuple(self.answers)))
            await message.channel.send(AnswerMsg)
            
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="disable", Error=e)
            self.config.update(f"{message.guild.id}.PastaEnabled", False) #Disables the plugin after an error to avoid spamming the logs
            pass
            
async def setup(bot : commands.Bot) :
    await bot.add_cog(CopyPasta(bot))
