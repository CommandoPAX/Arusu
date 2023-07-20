# Plugin contenant des utilitaires généraux

from discord.ext import commands
import os
import sys
from config import ArusuConfig

class Updater(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot
        self.config = ArusuConfig()

    @commands.command(name = "cog_update", usage = "", description = "Updates the bot, will restart the bot")
    async def Updater(self, ctx) :
        """
        Updates the bot, will restart the bot
        """
        try :
            await ctx.send("Updating bot...")
            os.system("git pull")
            print("------------------------------Restarting Bot------------------------------")
            await ctx.send("Restarting bot")
            os.execv(sys.executable, ['python'] + sys.argv) #the part that restarts the bot
        except Exception as e :
            await ctx.send("Could not update cogs")
            print(e)

async def setup(bot : commands.Bot) :
    await bot.add_cog(Updater(bot))
