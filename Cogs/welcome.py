# Plugin gérant les messages de bienvenue automatique

from discord.ext import commands
from config import ArusuConfig
from Core.ErrorHandler import LogError

class welcome(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot
        self.CogName = "welcome"
        self.config = ArusuConfig()
    
    @commands.command(name = "welcomeset", usage = "[channel ID]", description = "Sets the welcome channel")
    @commands.is_owner()
    async def welcomeset(self, ctx, channelID : int) :
        """
        Sets the welcome message channel
        """
        try :
            self.config.update(f"{ctx.guild.id}.welcome_channel", self.bot.get_channel(channelID).id)
            await ctx.send(f"Welcome channel set to {self.config.DATA[f'{ctx.guild.id}.welcome_channel']}")
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="welcomeset", Error=e)
            await ctx.send("Could not set welcome channel")

    @commands.command(name = "welcomemsg", usage = "[your welcome message]", description = "Sets the welcome message")
    @commands.is_owner()
    async def welcomemsg(self, ctx, welcomemsg) :
        """
        Sets the welcome message
        """
        try : 
            self.config.update(f"{ctx.guild.id}.welcome_message", welcomemsg)
            member = ctx.author
            await ctx.send("Welcome message set to : ")
            await ctx.send((self.config.DATA[f"{ctx.guild.id}.welcome_message"]).format(Member = member.mention, Server = ctx.guild))
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="welcomemsg", Error=e)
            await ctx.send("Could not set welcome message")

    @commands.command(name = "leaveset", usage = "[channel ID]", description = "Sets the leave channel")
    @commands.is_owner()
    async def leaveset(self, ctx, channelID : int) :
        """
        Sets the leave message channel
        """
        try :
            self.config.update(f"{ctx.guild.id}.leave_channel", self.bot.get_channel(channelID).id)
            await ctx.send(f"Leave channel set to {self.config.DATA[f'{ctx.guild.id}.leave_channel']}")
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="leaveset", Error=e)
            await ctx.send("Could not set leave channel")

    @commands.command(name = "leavemsg", usage = "[message]", description = "Sets the leave message")
    @commands.is_owner()
    async def leaveemsg(self, ctx, leavemsg) :
        """
        Sets the leave message
        """
        try : 
            self.config.update(f"{ctx.guild.id}.leave_message", leavemsg)
            member = ctx.author
            await ctx.send("Leave message set to : ")
            await ctx.send((self.config.DATA[f"{ctx.guild.id}.leave_message"]).format(Member = member.mention, Server = ctx.guild))
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="leavemsg", Error=e)
            await ctx.send("Could not set leave message")

    @commands.command(name = "welcome_test", usage = "", description = "Tests the welcome message using the author as the new member")
    @commands.is_owner()
    async def welcometest(self, ctx) :
        member = ctx.message.author
        channel = self.bot.get_channel(self.config.DATA[f'{member.guild.id}.welcome_channel'])
        await channel.send((self.config.DATA[f"{member.guild.id}.welcome_message"]).format(Member = member.mention(), Server = member.guild))

    @commands.command(name="leave_test", usage = "", description = "Tests the leave message using the author as the leaving member")
    @commands.is_owner()
    async def leavetest(self, ctx) :
        member = ctx.message.author
        channel = self.bot.get_channel(self.config.DATA[f'{member.guild.id}.leave_channel'])
        await channel.send((self.config.DATA[f"{member.guild.id}.leave_message"]).format(Member = member.mention(), Server = member.guild))

    ###################################################################################################################################

    @commands.Cog.listener(name = "on_member_join")
    async def welcome(self, member) :
        try : 
            channel = self.bot.get_channel(self.config.DATA[f'{member.guild.id}.welcome_channel'])
            await channel.send((self.config.DATA[f"{member.guild.id}.welcome_message"]).format(Member = member.mention, Server = member.guild))
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="on_member_join", Error=e)
    
    @commands.Cog.listener(name = "on_member_remove")
    async def leave(self, member) :
        try : 
            channel = self.bot.get_channel(self.config.DATA[f'{member.guild.id}.leave_channel'])
            await channel.send((self.config.DATA[f"{member.guild.id}.leave_message"]).format(Member = member.mention, Server = member.guild))
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="on_member_remove", Error=e)

async def setup(bot : commands.Bot) :
    await bot.add_cog(welcome(bot))
