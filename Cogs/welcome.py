# Plugin gérant les messages de bienvenue automatique

import discord
from discord.ext import commands
from config import ArusuConfig

class welcome(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot
        self.config = ArusuConfig()
    
    @commands.command(name = "welcomeset", usage = "[channel ID]", description = "Sets the welcome channel")
    @commands.is_owner()
    async def welcomeset(self, ctx) :
        """
        Sets the welcome message channel, currently only works on S;G France
        """
        try :
            self.config.update(f"{ctx.guild.id}.welcome_channel", self.bot.get_channel(482256698342506508).id)
            await ctx.send(f"Welcome channel set to {self.config.DATA[f'{ctx.guild.id}.welcome_channel']}")
        except Exception as e :
            await ctx.send("Could not set welcome channel")
            print(e)

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
            await ctx.send("Could not set welcome message")
            print(e)

    @commands.command(name = "leaveset", usage = "[channel ID]", description = "Sets the leave channel")
    @commands.is_owner()
    async def leaveset(self, ctx) :
        """
        Sets the leave message channel, currently only works on S;G France
        """
        try :
            self.config.update(f"{ctx.guild.id}.leave_channel", self.bot.get_channel(721312376225398785).id)
            await ctx.send(f"Leave channel set to {self.config.DATA[f'{ctx.guild.id}.leave_channel']}")
        except Exception as e :
            await ctx.send("Could not set leave channel")
            print(e)

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
            await ctx.send("Could not set leave message")
            print(e)

    ###################################################################################################################################

    @commands.Cog.listener(name = "on_member_join")
    async def welcome(self, ctx, member) :
        try : 
            channel = self.bot.get_channel(self.config.DATA[f'{ctx.guild.id}.welcome_channel'])
            await channel.send((self.config.DATA[f"{ctx.guild.id}.welcome_message"]).format(Member = discord.Member, serveur = ctx.guild))
        except :
            print("Could not send welcome message")
    
    @commands.Cog.listener(name = "on_member_remove")
    async def leave(self, ctx, member) :
        try : 
            channel = self.bot.get_channel(self.config.DATA[f'{ctx.guild.id}.leave_channel'])
            await channel.send((self.config.DATA[f"{ctx.guild.id}.leave_message"]).format(Member = discord.Member, serveur = ctx.guild))
        except :
            print("Could not send leave message")

async def setup(bot : commands.Bot) :
    await bot.add_cog(welcome(bot))
