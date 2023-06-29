# Plugin contenant des utilitaires généraux

import discord
from discord.ext import commands
import sys
import os

class utils(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot
    
    @commands.command(name = "ping", usage = "", description = "Pings the bot")
    async def ping(self, ctx:commands.Context):
        """
        Pings the bot
        """
        await ctx.send("Pong !")

    @commands.command(name = "restart", usage = "", description = "Restarts the bot")
    @commands.is_owner()
    async def restart(self, ctx) :
        """
        Restarts the bot
        """
        print("------------------------------Restarting Bot------------------------------")
        await ctx.send("Restarting bot...")
        os.execv(sys.executable, ['python'] + sys.argv) #the part that restarts the bot

    @commands.command(name = "shutdown", usage = "", description = "Shutdown the bot")
    @commands.is_owner()
    async def shutdown(self, ctx) :
        """
        shutdown the bot
        """
        try :
            await ctx.send("Shutting down...")
            await self.bot.close()
            print("------------------------------Shutting Down-------------------------------")
        except Exception as e :
            await ctx.send("Could not shut down bot")
            print(e)

    ###################################################################################################################################

    @commands.Cog.listener(name = "on_ready")
    async def ConfirmStart(self) :
        try :
            print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
            print('--------------------------------------------------------------------------')
        except :
            print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
            print("Not all plugins are online")
            print('--------------------------------------------------------------------------')

async def setup(bot : commands.Bot) :
    await bot.add_cog(utils(bot))
