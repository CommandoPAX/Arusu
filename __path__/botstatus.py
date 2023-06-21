# Plugin permettant de changer le statut du bot

import discord
from discord.ext import commands
import sys
import os

class botstatus(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot

    @commands.command(name ="streaming", usage = "[text]", description = "Changes the bot's status to 'Streaming [text]'")
    @commands.is_owner()
    async def streaming(self, ctx, customtxt) :
        """
        #Streaming status command
        """
        try :
            await ctx.bot.change_presence(status = discord.Status.dnd, activity = discord.Streaming(name = customtxt))
        except :
            await ctx.send("Could not change the bot's status")


    @commands.command(name ="playing", usage = "[text]", description = "Changes the bot's status to 'Playing [text]'")
    @commands.is_owner()
    async def playing(self, ctx, customtxt) :
        """
        #Playing status command
        """
        try :
            await ctx.bot.change_presence(status = discord.Status.dnd, activity = discord.Game(name = customtxt))
        except :
            await ctx.send("Could not change the bot's status")


    @commands.command(name ="listening", usage = "[text]", description = "Changes the bot's status to 'Listening to [text]'")
    @commands.is_owner()
    async def listening(self, ctx, customtxt) :
        """
        #Listening status command
        """
        try :
            await ctx.bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(name = customtxt, type = discord.ActivityType.listening))
        except :
            await ctx.send("Could not change the bot's status")


    @commands.command(name ="watching", usage = "[text]", description = "Changes the bot's status to 'Watching [text]'")
    @commands.is_owner()
    async def watching(self, ctx, customtxt) :
        """
        #Watching status command
        """
        try :
            await ctx.bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(name = customtxt, type = discord.ActivityType.watching))
        except :
            await ctx.send("Could not change the bot's status")

    @commands.command(name ="competing", usage = "[text]", description = "Changes the bot's status to 'Competing in [text]'")
    @commands.is_owner()
    async def competing(self, ctx, customtxt) :
        """
        #Competing status command
        """
        try :
            await ctx.bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(name = customtxt, type = discord.ActivityType.competing))
        except :
            await ctx.send("Could not change the bot's status")

async def setup(bot : commands.Bot) :
    await bot.add_cog(botstatus(bot))
