# Plugin contenant des utilitaires généraux

import discord
from discord.ext import commands

class utils(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot

    @commands.command(name="status", usage = "<usage>", description = "Change le statut du bot", help = "changes the bot's status")
    @commands.is_owner()
    async def status(self, ctx):
        """
        change le statut, à réimplémenter d'une manière qui marche
        """
        #await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Streaming("le code source d'Arusu"))
        await ctx.send("Statut changé")

    @commands.command(name = "ping", usage = "<usage>", description = "description", help = "Check to see if the bot is lagging")
    async def ping(self, ctx:commands.Context):
        """
        Ping le bot
        """
        await ctx.send("Pong !")

async def setup(bot : commands.Bot) :
    await bot.add_cog(utils(bot))
