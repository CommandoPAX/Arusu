# Plugin gérant les messages de bienvenue automatique

from discord.ext import commands
from Core.config import ArusuConfig
from Core.error_handler import LogError, ErrorEmbed

class Welcome(commands.Cog) :
    """
    Handles welcome and leave message
    """

    def __init__(self, bot) :
        self.bot = bot
        self.CogName = "Welcome"
        self.config = ArusuConfig()
    
    @commands.group(name = "welcome", description = "Base command")
    @commands.has_permissions(manage_channels = True, manage_messages = True)
    async def Welmain(self, ctx) :
        """
        Base command for setting the welcome message
        """
        pass
    
    @Welmain.command(name = "set", usage = "[channel ID]", description = "Sets the welcome channel")
    async def welcomeset(self, ctx, channelID : int) :
        """
        Sets the welcome message channel
        """
        try :
            self.config.update(f"{ctx.guild.id}.welcome_channel", self.bot.get_channel(channelID).id)
            await ctx.send(f"Welcome channel set to {self.config.DATA[f'{ctx.guild.id}.welcome_channel']}")
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="welcomeset", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not set welcome channel")

    @Welmain.command(name = "msg", usage = "[your welcome message]", description = "Sets the welcome message")
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
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not set welcome message")

    @Welmain.command(name = "test", usage = "", description = "Tests the welcome message using the author as the new member")
    async def welcometest(self, ctx) :
        try :
            member = ctx.message.author
            channel = self.bot.get_channel(self.config.DATA[f'{member.guild.id}.welcome_channel'])
            await channel.send((self.config.DATA[f"{member.guild.id}.welcome_message"]).format(Member = member.mention(), Server = member.guild))
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct= "welcome_test", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error in sending test message")

    @commands.group(name = "leave_2", description = "Base command")
    @commands.has_permissions(manage_channels = True, manage_messages = True)
    async def Leavemain(self, ctx) :
        """
        Base command for setting the leave message
        """
        pass

    @Leavemain.command(name = "set", usage = "[channel ID]", description = "Sets the leave channel")
    async def leaveset(self, ctx, channelID : int) :
        """
        Sets the leave message channel
        """
        try :
            self.config.update(f"{ctx.guild.id}.leave_channel", self.bot.get_channel(channelID).id)
            await ctx.send(f"Leave channel set to {self.config.DATA[f'{ctx.guild.id}.leave_channel']}")
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="leaveset", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not set leave channel")

    @Leavemain.command(name = "msg", usage = "[message]", description = "Sets the leave message")
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
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not set leave message")

    @Leavemain.command(name="test", usage = "", description = "Tests the leave message using the author as the leaving member")
    async def leavetest(self, ctx) :
        try :
            member = ctx.message.author
            channel = self.bot.get_channel(self.config.DATA[f'{member.guild.id}.leave_channel'])
            await channel.send((self.config.DATA[f"{member.guild.id}.leave_message"]).format(Member = member.mention(), Server = member.guild))
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="leavetest", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error in sending test message")

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
    await bot.add_cog(Welcome(bot))
