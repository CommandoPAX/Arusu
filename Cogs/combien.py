#Plugin qui permet au bot de répondre une valeur en centimes après qu'une phrase s'est fini par combien

from discord.ext import commands
import re
import random
import pycountry
from Core.config import ArusuConfig
from Core.error_handler import LogError, ErrorEmbed

class Combien(commands.Cog):
    """Combien ? 75 centimes"""
    
    def __init__(self, bot):
        self.bot = bot
        self.CogName = "Combien"
        self.config = ArusuConfig()
        
    @commands.group(name = "combien", description = "Main command to enable or disable the Combien Cog")
    @commands.has_permissions(manage_channels = True, manage_messages = True)
    async def combienmain(self, ctx) :
        """
        Main command to enable or disable the Combien Cog
        """
        pass
    
    @combienmain.command(name = "enable", usage = "", description = "Enables the cog")
    async def enable(self, ctx):
        """
        Enables the cog
        """
        try :
            self.config.update(f"{ctx.guild.id}.CombienEnabled", True)
            await ctx.send("Combien enabled")
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="enable", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error enabling the cog")
    
    @combienmain.command(name = "disable", usage = "", description = "Disables the cog")
    async def disable(self, ctx):
        """
        Disables the cog
        """
        try :
            self.config.update(f"{ctx.guild.id}.CombienEnabled", False)
            await ctx.send("Combien disabled")
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="disable", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error disabling the cog")

    ################################################################################################################################### 
    
    @commands.Cog.listener(name = "on_message")
    async def CombienAnswer(self, message):
        try :
            if message.author.id == self.bot.user.id:  #Stopping the bot from reading its own message
                return
            if self.config.DATA[f"{message.guild.id}.CombienEnabled"] != True : 
                return
            #Check if "combien" is written
            if re.search(r"\bcombien\b\W*$",message.content, flags=re.I) :
                argent = random.randint(1,1000000)
                isMil = ""
                if random.random() > 0.8 :
                    isMil = " millions de"
                else :
                    isMil = ""
                random.randint(0,len(pycountry.countries)-1)
                await message.channel.send(str(argent)+isMil+" centimes "+list(pycountry.currencies)[random.randint(0,len(pycountry.currencies)-1)].alpha_3)
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="listener", Error=e)
            self.config.update(f"{message.guild.id}.CombienEnabled", False) #Disables the plugin after an error to avoid spamming the logs
            pass
            
async def setup(bot : commands.Bot) :
    await bot.add_cog(Combien(bot))