import os
import discord
from discord.ext import commands
from .plugins import *

TOKEN = os.getenv('DISCORD_TOKEN')
#client = discord.Client()

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready(self, bot):
    await bot.load("PluginManager") #load PluginManager

#client.run(TOKEN)
bot.run(TOKEN)
