import os
import discord
from .plugins import *

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print("Hello World")

client.run(TOKEN) #Run le bot
