import discord
import re
import random
from discord.ext import commands

list = ["Quoi", "quoi", "Quoi ?", "quoi ?"]

message = discord.Message

class Feur(commands.Cog):
    """Quoi ? Feur"""
    
    def __init__(self, bot):
        self.bot = bot
        
    def setup(bot) :
        bot.add_cog(Feur(bot))
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == discord.Client().user:  #Stopping the bot from reading its on message
            return None
        for l in list :
            if message.content.endswith(l) == True : 
                    await message.channel.send("Feur")
            else :
                pass