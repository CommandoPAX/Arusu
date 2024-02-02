# Handles changing the bot's status and auto setting it

import discord
from discord.ext import commands
from Core.config import ArusuConfig
from Core.error_handler import LogError, ErrorEmbed

class Botstatus(commands.Cog) :
    """
    Handles changing the bot status
    """

    def __init__(self, bot) :
        self.bot = bot
        self.config = ArusuConfig()
        self.CogName = "Botstatus"
    
    @commands.command(name = "status", usage = '["status"] ["activity"] ["additionnal text"]', description = "Updates Arusu's status")
    @commands.is_owner()
    async def status_main(self, ctx, status, activity, AdditText = "le code source d'Arusu") :
        """
        Main command to change Arusu's status, handles status, activity and additionnal text
        """
        try :
            if status == "dnd" :
                self.config.update("BOT_STATUS", "dnd")
                STATUS = discord.Status.dnd
            if status == "online" :
                self.config.update("BOT_STATUS", "online")
                STATUS = discord.Status.online
            if status == "idle" :
                self.config.update("BOT_STATUS", "idle")
                STATUS = discord.Status.idle
            if status == "offline" :
                self.config.update("BOT_STATUS", "offline")
                STATUS = discord.Status.offline
        except Exception as e:
            LogError(self.CogName, "status_main", e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Invalid status. Available choices : dnd, online, idle, offline")

        try :
            if activity == "playing" :
                self.config.update("BOT_ACTIVITY", "playing")
                self.config.update("BOT_ACTIVITY_TEXT", AdditText)
                ACTIVITY = discord.Game(name = AdditText)
            if activity == "listening" :
                self.config.update("BOT_ACTIVITY", "listening")
                self.config.update("BOT_ACTIVITY_TEXT", AdditText)
                ACTIVITY = discord.Activity(name = AdditText, type = discord.ActivityType.listening)
            if activity == "watching" :
                self.config.update("BOT_ACTIVITY", "watching")
                self.config.update("BOT_ACTIVITY_TEXT", AdditText)
                ACTIVITY = discord.Activity(name = AdditText, type = discord.ActivityType.watching)
            if activity == "competing" :
                self.config.update("BOT_ACTIVITY", "competing")
                self.config.update("BOT_ACTIVITY_TEXT", AdditText)
                ACTIVITY = discord.Activity(name = AdditText, type = discord.ActivityType.competing)
        except : 
            LogError(self.CogName, "status_main", e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Invalid status. Available choices : playing, listening, watching, competing")

        try :
            await self.bot.change_presence(status = STATUS, activity = ACTIVITY)
            await ctx.send(f"Bot status changed to : {STATUS}, {ACTIVITY}")
        except :
            LogError(self.CogName, "status_main", e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error in chaning the bot status at final step")

    ################################################################################################################################### 

    @commands.Cog.listener(name = "on_ready")
    async def basestatus(self) :
        try :
            if self.config.DATA["BOT_STATUS"] == "dnd" :
                STATUS = discord.Status.dnd
            if self.config.DATA["BOT_STATUS"] == "online" :
                STATUS = discord.Status.online
            if self.config.DATA["BOT_STATUS"] == "idle" :
                STATUS = discord.Status.idle
            if self.config.DATA["BOT_STATUS"] == "offline" :
                STATUS = discord.Status.offline
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="bot_status_listener", Error=e)

        try :
            if self.config.DATA["BOT_ACTIVITY"] == "playing" :
                ACTIVITY = discord.Game(name = self.config.DATA["BOT_ACTIVITY_TEXT"])
            if self.config.DATA["BOT_ACTIVITY"] == "listening" :
                ACTIVITY = discord.Activity(name = self.config.DATA["BOT_ACTIVITY_TEXT"], type = discord.ActivityType.listening)
            if self.config.DATA["BOT_ACTIVITY"] == "watching" :
                ACTIVITY = discord.Activity(name = self.config.DATA["BOT_ACTIVITY_TEXT"], type = discord.ActivityType.watching)
            if self.config.DATA["BOT_ACTIVITY"] == "competing" :
                ACTIVITY = discord.Activity(name = self.config.DATA["BOT_ACTIVITY_TEXT"], type = discord.ActivityType.competing)
        except Exception as e: 
            LogError(CogName=self.CogName, CogFunct="bot_activity_listener", Error=e)
        
        try :
            await self.bot.change_presence(status = STATUS, activity = ACTIVITY)
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="bot_status_change_listener", Error=e)

async def setup(bot : commands.Bot) :
    await bot.add_cog(Botstatus(bot))
