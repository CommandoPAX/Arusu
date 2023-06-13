import discord
from discord.ext import commands
import re
import random

message = discord.Message

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
        if message.author == discord.Client().user:  #Stopping the bot from reading its on message
            return None
        #Check if "quoi" is write
        if re.search("*[qQ][uU][oO0][iI1]*",message.content) :
                #Cases for "quoi" and "pourquoi" and "pour quoi"
                if re.search("*[pP][oO0][rR]\s?[qQ][uU][oO0][iI1]*",message.content) :
                    await message.channel.send("Pour feur")
                else:
                    await message.channel.send("Feur")
