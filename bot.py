#Core d'Arusu

import os
import discord
import asyncio
from discord.ext import commands

TOKEN = "TOKEN"

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all()) #set le prefix et les intents

async def load() :
    for root,dirs,files in os.walk("./__path__"): #check le dossier plugins pour chaque fichier
        for filename in files : 
            if filename.endswith(".py"): #sinon c'est pas des modules
                try : 
                    await bot.load_extension(f"__path__.{filename[:-3]}") #ajoute le module au bot
                except Exception as e:
                    print("Extension not loaded : ", filename, "\n")
                    print(e)
                
async def main(): #fonction qui load les modules et démarre le bot
    await load()
    await bot.start(TOKEN) #démarre le bot

asyncio.run(main())
