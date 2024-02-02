# Answers "Feur" if a message ends with "Quoi"

from discord.ext import commands
import re
from Core.config import ArusuConfig
from Core.error_handler import LogError, ErrorEmbed

class Feur(commands.Cog):
    """Quoi ? Feur"""
    
    def __init__(self, bot):
        self.bot = bot
        self.CogName = "Feur"
        self.config = ArusuConfig()
        
    @commands.group(name = "feur", description = "Main command to enable or disable the Feur Cog")
    @commands.has_permissions(manage_channels = True, manage_messages = True)
    async def feurmain(self, ctx) :
        """
        Main command to enable or disable the Feur Cog
        """
        pass
    
    @feurmain.command(name = "enable", usage = "", description = "Enables the cog")
    async def enable(self, ctx):
        """
        Enables the cog
        """
        try :
            self.config.update(f"{ctx.guild.id}.FeurEnabled", True)
            await ctx.send("Feur enabled")
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="enable", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error enabling the cog")
    
    @feurmain.command(name = "disable", usage = "", description = "Disables the cog")
    async def disable(self, ctx):
        """
        Disables the cog
        """
        try :
            self.config.update(f"{ctx.guild.id}.FeurEnabled", False)
            await ctx.send("Feur disabled")
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="disable", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error disabling the cog")

    ################################################################################################################################### 
    
    @commands.Cog.listener(name = "on_message")
    async def FeurAnswer(self, message):
        try :
            if message.author.id == self.bot.user.id:  #Stopping the bot from reading its own message
                return
            if self.config.DATA[f"{message.guild.id}.FeurEnabled"] != True : 
                return
            #Check if "quoi" is written
            if re.search(r"\bquoi\b\W*$",message.content, flags=re.I) :
                #Cases for "quoi" and "pourquoi" and "pour quoi"
                await message.reply("Feur")
            if re.search(r"\bpour ?quoi\b\W*$",message.content, flags=re.I) :
                await message.reply("Pour feur")
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="listener", Error=e)
            self.config.update(f"{message.guild.id}.FeurEnabled", False) #Disables the plugin after an error to avoid spamming the logs
            pass
            
async def setup(bot : commands.Bot) :
    await bot.add_cog(Feur(bot))
