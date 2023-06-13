# Plugin contenant des utilitaires généraux

import discord
from discord.ext import commands

class utilities(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Streaming("le code source d'Arusu"))
        print("Arusu Dev is Online")