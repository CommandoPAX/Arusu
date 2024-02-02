# Handles updating the bot
# This is a core cog, do not touch

from discord.ext import commands
import os
import sys
from Core.config import ArusuConfig
from Core.error_handler import LogError, ErrorEmbed

class Updater(commands.Cog) :
    """
    Handles updating the bot
    """

    def __init__(self, bot) :
        self.bot = bot
        self.CogName = "Updater"
        self.config = ArusuConfig()

    @commands.command(name = "cog_update", usage = "", description = "Updates the bot, will restart the bot")
    @commands.is_owner()
    async def Updater(self, ctx) :
        """
        Updates the bot, will restart the bot
        """
        try :
            await ctx.send("Updating bot...")
            os.system("git pull")
            print("------------------------------Restarting Bot------------------------------")
            await ctx.send("Restarting bot")
            os.execv(sys.executable, ['python3'] + sys.argv) #the part that restarts the bot
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="cog_update", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error updating the bot")

async def setup(bot : commands.Bot) :
    await bot.add_cog(Updater(bot))
