# Plugin contenant l'autoroler ainsi que le selfrole

import discord
from discord.ext import commands

class autoroler(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot
        self.selfrolelist = {}
        self.autorolelist = {}
    
    @commands.command(name = "autoroleset", usage = "[Role ID]", description = "Sets a role to be given to new members")
    async def autoroleset(self, ctx, autoroleID) :
        """
        Sets a role to be given to new members
        """
        self.autorolelist #j'ai la flemme, va mourir Corusu du futur je te hais

async def setup(bot : commands.Bot) :
    await bot.add_cog(autoroler(bot))