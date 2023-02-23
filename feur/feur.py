from redbot.core import commands
import discord
import re
from redbot.core.commands import Cog

list = ["Quoi", "quoi"]

class Feur(commands.Cog):
    """Quoi ? Feur"""
    activate = False

    def __init__(self, bot):
        self.bot = bot
    @commands.group(name = "feur", invoque_without_command = True)
    async def feurmain(self, ctx) :
        pass
    @feurmain.command(name = "activate")
    async def actimain(self, ctx) :
        if activate == True : 
            activate = False
            await ctx.send("Feur désactivé")
        else :
            activate = True
            await ctx.send("Feur activé")
     
    @Cog.listener()
    async def on_message(message : discord.Message):
        if activate == True :
            for l in list :
                if re.search(l, message.content) :
                    await ctx.send("Feur")
                else : 
                    pass
        else :
            pass
    
    
