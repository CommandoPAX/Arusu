#Plugin qui permet au bot de répondre feur après un message se terminant par quoi

import discord
from discord.ext import commands
import re
import random

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
    async def on_message(self, ctx, message, feuractive):
        if message.author == discord.Client().user:  #Stopping the bot from reading its on message
            return 
        if feuractive != True : 
            return
        #Check if "quoi" is written
        if re.search("*[qQ][uU][oO0][iI1]*",message.content) :
            #Cases for "quoi" and "pourquoi" and "pour quoi"
            if re.search("*[pP][oO0][rR]\s?[qQ][uU][oO0][iI1]*",message.content) :
                await ctx.send("Pour feur")
            else:
                await ctx.send("Feur")

async def setup(bot : commands.Bot) :
    await bot.add_cog(Feur(bot))
