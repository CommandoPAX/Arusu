# Plugin contenant des utilitaires généraux

import discord
from discord.ext import commands
import sys
import os
from config import ArusuConfig
from Core.ErrorHandler import LogError, ErrorEmbed

class Utils(commands.Cog) :
    """
    Useful commands that don't fit in another cog
    """

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
        try :
            print("------------------------------Restarting Bot------------------------------")
            await ctx.send("Restarting bot...")
            os.execv(sys.executable, ['python3'] + sys.argv) #Restarts the shell using the same argument as before
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="restart", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not restart bot")
        
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
            LogError(CogName=self.CogName, CogFunct="shutdown", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not shutdown bot, weird")

    @commands.group(name = "utils", description = "Base command")
    @commands.is_owner()
    async def utils(self, ctx) :
        """
        Base command for diferent utils
        """
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
        except Exception as e: 
            LogError(CogName=self.CogName, CogFunct="embed_colour_set", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not set new embed color")

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
                LogError(CogName=self.CogName, CogFunct="showset", Error=e)
                await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not get settings from config file")

            embed = (discord.Embed(title="Settings",
                                description=Settings,
                                color = discord.Color.from_str(self.config.DATA["BOT_EMBED_COLOUR"])))
            await ctx.send(embed = embed)
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="prefixset", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not send Arusu's config")

    @utils.command(name = "prefix", usage = "[prefix]", description = "Changes Arusu's prefix, requires a restart to take effect")
    async def prefixset(self, ctx, NEWPREFIX) :
        try :
            self.config.update("BOT_PREFIX", str(NEWPREFIX))
            await ctx.send(f"Prefix changed to {NEWPREFIX}")
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="prefixset", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not change prefix")

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
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error has been logged")
            
    @utils.command(name = "get_logs", usage = "[YYYY-MM-DD]", description = "Returns the logs for a given date")
    async def GetLogs(self, ctx, LOGSDATE : str) : 
        """
        Returns the logs for a given date. Date format : YYYY-MM-DD
        """
        try : 
            TBS = ""
            f = open("Logs/" + LOGSDATE + ".log", "r")
            for line in f.readlines() :
                TBS = TBS + line + "\n"
            await ctx.send(embed = discord.Embed(title= LOGSDATE, description=TBS))
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="GetLogs", Error = e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not find or access logs")

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
            
    @commands.Cog.listener(name="on_command_error")
    async def ErrorHandlerV2(self, ctx : commands.Context, ERROR : Exception) : #Handles missing commands error message
        try :
            if isinstance(ERROR, commands.CommandNotFound) :
                await ErrorEmbed(ctx, ERROR)
            else : 
                pass
        except :
            LogError(self.CogName, "ErrorHandlerV2", ERROR)

async def setup(bot : commands.Bot) :
    await bot.add_cog(Utils(bot))
