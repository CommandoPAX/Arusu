#Core d'Arusu

import os
import asyncio
from Core.initializer import ArusuInit
from Core.error_handler import LogError
from Core.config import ArusuConfig

async def load(bot) :
    config = ArusuConfig()
    for root,dirs,files in os.walk("./Cogs"): #This check the directory for files
        files.sort()
        for filename in files : 
            if filename.endswith(".py") and filename !="chat.py" : #We check for cogs and filter unwanted cogs
                try : 
                    await bot.load_extension(f"Cogs.{filename[:-3]}") #We add the cog to the bot
                except Exception as e:
                    print("Extension not loaded : ", filename, "\n")
                    LogError(CogName="Main", CogFunct="load", Error=e)
            if "AI_ENABLED" in config.DATA.keys() : #Used to enable / disable the chat cog
                if config.DATA["AI_ENABLED"] == True :
                    try :
                        await bot.load_extension(f"Cogs.chat")
                    except Exception as e:
                        print("Extension not loaded : ", filename, "\n")
                        LogError(CogName="Main", CogFunct="load", Error=e)
            elif "AI_ENABLED" not in config.DATA.keys() :
                config.update("AI_ENABLED", False)

async def main() :
    initializer = ArusuInit(willListen=True)
    Arusu_Bot = initializer.getBot()
    await load(Arusu_Bot)
    await Arusu_Bot.startBot()

asyncio.run(main())
