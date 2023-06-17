# Plugin contenant des utilitaires généraux

import discord
from discord.ext import commands

class utils(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot

    @commands.command(name="status", usage = "<usage>", description = "Change le statut du bot")
    @commands.is_owner()
    async def status(self, ctx):
        #await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Streaming("le code source d'Arusu"))
        await ctx.send("Arusu Dev is Online")

    @commands.command(name = "ping", usage = "<usage>", description = "description")
    async def ping(self, ctx:commands.Context):
        await ctx.send("Pong !")

async def setup(bot : commands.Bot) :
    await bot.add_cog(utils(bot))