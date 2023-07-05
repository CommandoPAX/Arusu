#Core d'Arusu

import os
import discord
import asyncio
from discord.ext import commands
from ArusuInitializer import ArusuInit
from ArusuBot import Arusu
from help import HelpCommand

async def load(bot) :
    for root,dirs,files in os.walk("./__path__"): #check le dossier plugins pour chaque fichier
        for filename in files : 
            if filename.endswith(".py") and filename !="config.py": #sinon c'est pas des modules
                try : 
                    await bot.load_extension(f"__path__.{filename[:-3]}") #ajoute le module au bot
                except Exception as e:
                    print("Extension not loaded : ", filename, "\n")
                    print(e)
    try : 
        await bot.load_extension(f"__path__.chatter.chat")
    except :
        print("Chatter n'a pas pu être load")
        #print(Exception)

async def main() :
    initializer = ArusuInit(willListen=True)
    Arusu_Bot = initializer.getBot()
    await load(Arusu_Bot)
    await Arusu_Bot.startBot()

asyncio.run(main())
