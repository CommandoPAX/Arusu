# Plugin gérant les messages de bienvenue automatique

import discord
from discord.ext import commands

class welcome(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot
        self.wchannel = 0
        self.lchannel = 0
        self.WelcomeMSG = f"Bienvenue dans le serveur {discord.Member}"
        self.LeaveMSG = f"{discord.Member} a quitté le serveur."
    
    @commands.command(name = "welcomeset", usage = "[channel ID]", description = "Sets the welcome channel")
    @commands.is_owner()
    async def welcomeset(self, ctx, channelID) :
        """
        Sets the welcome message channel, 0 to disable
        """
        self.wchannel = self.bot.get_channel(channelID)
        await ctx.send(f"Welcome channel set to {self.wchannel}")

    @commands.command(name = "welcomemsg", usage = "[your welcome message]", description = "Sets the welcome message")
    @commands.is_owner()
    async def welcomemsg(self, ctx, message) :
        """
        Sets the welcome message
        """
        self.WelcomeMSG = message
        await ctx.send("Welcome message set to : ", self.WelcomeMSG)

    @commands.command(name = "leaveset", usage = "[channel ID]", description = "Sets the leave channel")
    @commands.is_owner()
    async def leaveset(self, ctx, channelID) :
        """
        Sets the leave message channel, 0 to disable
        """
        self.lchannel = self.bot.get_channel(channelID)
        await ctx.send(f"Welcome channel set to {self.lchannel}")

    @commands.command(name = "leavemsg", usage = "[message]", description = "Sets the leave message")
    @commands.is_owner()
    async def leaveemsg(self, ctx, message) :
        """
        Sets the leave message
        """
        self.LeaveMSG = message
        await ctx.send("Welcome message set to : ", self.LeaveMSG)

    ###################################################################################################################################

    @commands.Cog.listener(name = "on_member_join")
    async def welcome(self, member) :
        try : 
            if self.wchannel != 0 :
                await self.wchannel.send(self.WelcomeMSG)
            else : 
                pass
        except Exception as e :
            print(e)
    
    @commands.Cog.listener(name = "on_member_remove")
    async def leave(self, member) :
        try : 
            if self.lchannel != 0 :
                await self.lchannel.send(self.LeaveMSG)
            else : 
                pass
        except Exception as e :
            print(e)

async def setup(bot : commands.Bot) :
    await bot.add_cog(welcome(bot))