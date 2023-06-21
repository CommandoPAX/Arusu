#Plugin qui permet au bot de répondre feur après un message se terminant par quoi

import discord
from discord.ext import commands
import re
import random

class Feur(commands.Cog):
    """Quoi ? Feur"""
    
    def __init__(self, bot):
        self.bot = bot
        self.feuractive = True
        
    @commands.group(name = "feur", invoque_without_command = True)
    async def feurmain(self, ctx) :
        pass
    
    @feurmain.command(name = "enable", usage = "", description = "Active le cog")
    async def enable(self, ctx):
        """Active le cog"""
        if self.feuractive == True :
            await ctx.send("Feur était déjà activé.")
        else : 
            self.feuractive = True
            await ctx.send(("Feur activé"))
    
    @feurmain.command(name = "disable", usage = "", description = "Désactive le plugin")
    async def disable(self, ctx):
        """Désactive le plugin"""
        if self.feuractive == False :
            await ctx.send("Feur était déjà desactivé.")
        else : 
            self.feuractive = False
            await ctx.send(("Feur désactivé"))

    ################################################################################################################################### 
    
    @commands.Cog.listener(name = "on_message")
    async def FeurAnswer(self, message):
        if message.author.id == self.bot.user.id:  #Stopping the bot from reading its own message
            return
        if self.feuractive == False : 
            return
        #Check if "quoi" is written
        if re.search(r"[\s\S]*?\bquoi\b\W*$",message.content, flags=re.I) :
            #Cases for "quoi" and "pourquoi" and "pour quoi"
            await message.channel.send("Feur")
        if re.search(r"[\s\S]*\bpour ?quoi\b\W*$",message.content, flags=re.I) :
            await message.channel.send("Pour feur")
            

async def setup(bot : commands.Bot) :
    await bot.add_cog(Feur(bot))
