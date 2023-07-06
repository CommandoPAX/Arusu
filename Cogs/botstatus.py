# Plugin permettant de changer le statut du bot

import discord
from discord.ext import commands
import sys
import os

class botstatus(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot

    @commands.command(name ="playing", usage = "[text]", description = "Changes the bot's status to 'Playing [text]'")
    @commands.is_owner()
    async def playing(self, ctx, customtxt) :
        """
        #Playing status command
        """
        try :
            await ctx.bot.change_presence(status = discord.Status.dnd, activity = discord.Game(name = customtxt))
        except Exception as e:
            await ctx.send("Could not change the bot's status")
            print(e)


    @commands.command(name ="listening", usage = "[text]", description = "Changes the bot's status to 'Listening to [text]'")
    @commands.is_owner()
    async def listening(self, ctx, customtxt) :
        """
        #Listening status command
        """
        try :
            await ctx.bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(name = customtxt, type = discord.ActivityType.listening))
        except Exception as e:
            await ctx.send("Could not change the bot's status")
            print(e)


    @commands.command(name ="watching", usage = "[text]", description = "Changes the bot's status to 'Watching [text]'")
    @commands.is_owner()
    async def watching(self, ctx, customtxt) :
        """
        #Watching status command
        """
        try :
            await ctx.bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(name = customtxt, type = discord.ActivityType.watching))
        except Exception as e:
            await ctx.send("Could not change the bot's status")
            print(e)

    @commands.command(name ="competing", usage = "[text]", description = "Changes the bot's status to 'Competing in [text]'")
    @commands.is_owner()
    async def competing(self, ctx, customtxt) :
        """
        #Competing status command
        """
        try :
            await ctx.bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(name = customtxt, type = discord.ActivityType.competing))
        except Exception as e:
            await ctx.send("Could not change the bot's status")
            print(e)

    ################################################################################################################################### 

    @commands.Cog.listener(name = "on_ready")
    async def basestatus(self) :
        await self.bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(name = "le code source d'Arusu", type = discord.ActivityType.watching))

async def setup(bot : commands.Bot) :
    await bot.add_cog(botstatus(bot))