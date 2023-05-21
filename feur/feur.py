from redbot.core import commands, Config
import discord
import re
import random
from redbot.core.commands import Cog
from redbot.core.bot import Red

list = ["Quoi", "quoi", "Quoi ?", "quoi ?"]

message = discord.Message
client = discord.Client()

class Feur(commands.Cog):
    """Quoi ? Feur"""
    
    def __init__(self, bot: Red):
        self.bot = bot
        
    @commands.group(name = "feur", invoque_without_command = True)
    async def feurmain(self, ctx) :
        pass
    
    @feurmain.command()
    async def enable(self, ctx):
        """Active le plugin"""
        await self.config.guild(ctx.guild).enabled.set(True)
        await ctx.send(("Feur activé"))
    
    @feurmain.command()
    async def disable(self, ctx):
        """Désactive le plugin"""
        await self.config.guild(ctx.guild).enabled.set(False)
        await ctx.send(("Feur désactivé"))
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == client.user:  #Stopping the bot from reading its on message
            return None
        for l in list :
            if message.content.endswith(l) == True : 
                    await message.channel.send("Feur")
            else :
                pass
