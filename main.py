#Core d'Arusu

import os
import asyncio
from ArusuInitializer import ArusuInit
from Core.ErrorHandler import LogError

async def load(bot) :
    for root,dirs,files in os.walk("./Cogs"): #check le dossier plugins pour chaque fichier
        for filename in files : 
            if filename.endswith(".py") and filename !="config.py": #sinon c'est pas des modules
                try : 
                    await bot.load_extension(f"Cogs.{filename[:-3]}") #ajoute le module au bot
                except Exception as e:
                    print("Extension not loaded : ", filename, "\n")
                    LogError(CogName="Main", CogFunct="load", Error=e)

async def main() :
    initializer = ArusuInit(willListen=True)
    Arusu_Bot = initializer.getBot()
    await load(Arusu_Bot)
    await Arusu_Bot.startBot()

asyncio.run(main())
