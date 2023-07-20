#Plugin qui permet au bot de répondre feur après un message se terminant par quoi

from discord.ext import commands
import re
from config import ArusuConfig

class Feur(commands.Cog):
    """Quoi ? Feur"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = ArusuConfig()
        
    @commands.group(name = "feur")
    @commands.is_owner()
    async def feurmain(self, ctx) :
        pass
    
    @feurmain.command(name = "enable", usage = "", description = "Active le cog")
    async def enable(self, ctx):
        """Active le cog"""
        try :
            if self.config.DATA[f"{ctx.guild.id}.FeurEnabled"] == 1:
                await ctx.send("Feur était déjà activé.")
            else : 
                self.config.update(f"{ctx.guild.id}.FeurEnabled", 1)
                await ctx.send(("Feur activé"))
        except Exception as e:
            print(e)
    
    @feurmain.command(name = "disable", usage = "", description = "Désactive le plugin")
    async def disable(self, ctx):
        """Désactive le plugin"""
        try :
            if self.config.DATA[f"{ctx.guild.id}.FeurEnabled"] == 0 :
                await ctx.send("Feur était déjà desactivé.")
            else : 
                self.config.update(f"{ctx.guild.id}.FeurEnabled", 0)
                await ctx.send(("Feur désactivé"))
        except Exception as e:
            print(e)

    ################################################################################################################################### 
    
    @commands.Cog.listener(name = "on_message")
    async def FeurAnswer(self, message):
        try :
            if message.author.id == self.bot.user.id:  #Stopping the bot from reading its own message
                return
            if self.config.DATA[f"{message.guild.id}.FeurEnabled"] != 1 : 
                return
            #Check if "quoi" is written
            if re.search(r"\bquoi\b\W*$",message.content, flags=re.I) :
                #Cases for "quoi" and "pourquoi" and "pour quoi"
                await message.channel.send("Feur")
            if re.search(r"\bpour ?quoi\b\W*$",message.content, flags=re.I) :
                await message.channel.send("Pour feur")
        except :
            pass
            
async def setup(bot : commands.Bot) :
    await bot.add_cog(Feur(bot))
