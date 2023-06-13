#Core d'Arusu

import os
import discord
import asyncio
from discord.ext import commands

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) #Apparament un bug connu sur Windows

TOKEN = "OTAzNjcwODM4NDM4NTU5ODA2.GaLZnB.2iZ-uhX41-PzDRyAMhA7-BsXVM_SJ6WET-LOlY"

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all()) #set le prefix et les intents

async def load() :
    for filename in os.listdir("./plugins"): #check le dossier plugins pour chaque fichier
        if filename.endswith(".py"): #sinon c'est pas des modules
            await bot.load_extension(f"plugins.{filename[:-3]}") #ajoute le module au bot

async def main(): #fonction qui load les modules et démarre le bot
    await load()
    await bot.start(TOKEN) #démarre le bot

asyncio.run(main())
