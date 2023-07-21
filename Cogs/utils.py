# Plugin contenant des utilitaires généraux

import discord
from discord.ext import commands
import sys
import os
from config import ArusuConfig
from Core.ErrorHandler import LogError

class utils(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot
        self.config = ArusuConfig()
        self.CogName = "utils"
        
    @commands.command(name = "ping", usage = "", description = "Pings the bot")
    async def ping(self, ctx:commands.Context):
        """
        Pings the bot
        """
        await ctx.send("Pong !")

    @commands.command(name = "restart", usage = "", description = "Restarts the bot", aliases = ["r"])
    @commands.is_owner()
    async def restart(self, ctx) :
        """
        Restarts the bot
        """
        print("------------------------------Restarting Bot------------------------------")
        await ctx.send("Restarting bot...")
        os.execv(sys.executable, ['python'] + sys.argv) #the part that restarts the bot

    @commands.command(name = "shutdown", usage = "", description = "Shutdown the bot", aliases = ["sleep_time"])
    @commands.is_owner()
    async def shutdown(self, ctx) :
        """
        shutdown the bot
        """
        try :
            await ctx.send("Shutting down...")
            print("------------------------------Shutting Down-------------------------------")
            await self.bot.close()
        except Exception as e :
            await ctx.send("Could not shut down bot")
            print(e)

    @commands.group(name = "utils")
    @commands.is_owner()
    async def utils(self, ctx) :
        pass

    @utils.command(name = "config_test", usage = "", description = "Tests the config plugin")
    async def conftest(self, ctx) :
        """
        Tests Arusu's config
        """
        try :
            await ctx.send(self.config.DATA[f"{ctx.guild.id}.Base"])
        except :
            self.config.update(f"{ctx.guild.id}.Base", "Arusu's config working")
            await ctx.send(self.config.DATA[f"{ctx.guild.id}.Base"])

    @utils.command(name = "embed_colour", usage = "", description = "Changes the embed default color")
    async def embed_colour_set(self, ctx, colour = "#1900ff") :
        self.config.update("BOT_EMBED_COLOUR", colour)
        try :
            embed = discord.Embed(title="Default Embed", description=f"Colour changed to {colour}", color=discord.Color.from_str(colour))
            await ctx.send(embed = embed)
        except : 
            await ctx.send("Invalid colour")

    @utils.command(name = "showsettings", usage = "", description = "Shows Arusu's config")
    async def showset(self, ctx) : 
        """
        Show Arusu's config
        """
        try :
            Settings = ""
            try :
                for i in self.config.DATA.keys() :
                    if i != "BOT_TOKEN" :
                        Settings += f"**{i}** : {self.config.DATA[i]} \n"
            except Exception as e :
                print("Error : error in Settings generation")
                print(e)

            embed = (discord.Embed(title="Settings",
                                description=Settings,
                                color = discord.Color.from_str(self.config.DATA["BOT_EMBED_COLOUR"])))
        except Exception as e :
            print("Error : error in embed settings generation")
            print(e)
        await ctx.send(embed = embed)

    @utils.command(name = "prefix", usage = "[prefix]", description = "Changes Arusu's prefix, requires a restart to take effect")
    async def prefixset(self, ctx, NEWPREFIX) :
        try :
            self.config.update("BOT_PREFIX", str(NEWPREFIX))
            await ctx.send(f"Prefix changed to {NEWPREFIX}")
        except Exception as e :
            await ctx.send("Could not change prefix")
            print("Error in changing prefix")
            print(e)

    @utils.command(name = "error_test", usage = "", description = "Creates an artifical error that will be logged")
    async def ErrorTest(self, ctx) :
        """
        Creates an artifical error that will be logged
        """
        try :
            await ctx.send("Creating an artifical error...")
            #Next line has an error, this is normal and is meant to trigger LogError
            print(ThisWillReturnAnError) # type: ignore
        except Exception as e :
            LogError(CogName= self.CogName, CogFunct= "ErrorTest", Error=e)

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
