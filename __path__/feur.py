#Plugin qui permet au bot de répondre feur après un message se terminant par quoi

import discord
from discord.ext import commands
import re
import random

list = ["Quoi", "quoi", "Quoi ?", "quoi ?"]

class Feur(commands.Cog):
    """Quoi ? Feur"""
    
    def __init__(self, bot):
        self.bot = bot
        message = discord.Message
        feuractive = True
        
    @commands.group(name = "feur", invoque_without_command = True)
    async def feurmain(self, ctx) :
        pass
    
    @feurmain.command()
    async def enable(self, ctx):
        """Active le plugin"""
        feuractive = True
        await ctx.send(("Feur activé"))
    
    @feurmain.command()
    async def disable(self, ctx):
        """Désactive le plugin"""
        feuractive = False
        await ctx.send(("Feur désactivé"))
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == discord.Client().user:  #Stopping the bot from reading its own message
            return 
        #Check if "quoi" is written
        if re.search(r".*quoi.*",message.content, flags=re.I) :
            #Cases for "quoi" and "pourquoi" and "pour quoi"
            if re.search(r".*pour\s?quoi.*",message.content, flags=re.I) :
                await message.channel.send("Pour feur")
            else:
                await message.channel.send("Feur")

    @commands.Cog.listener() #J'ai test avec l'ancienne version, ca marche pas du tout
    async def on_message(self, message):
        if message.author == discord.Client().user:  #Stopping the bot from reading its on message
            return None
        for l in list :
            if message.content.endswith(l) == True : 
                    await message.channel.send("Feur")
            else :
                pass

async def setup(bot : commands.Bot) :
    await bot.add_cog(Feur(bot))
